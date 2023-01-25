# coding: utf-8
# Instax send/recieve Program for python3
#
# 2017/07/12 - 2020/12/24
# coding by S.Sonoda, N.Tanaka and H.Yoshizawa

import struct
import logging

# pip install enum34 for python2.7
from enum import Enum, IntEnum
import numpy as np
from retry import retry

import cv2
import os
import glob

from util.encryption import decode_cipher, key_load, cipher_text
from util.find_com_number import find_usb_device # for windows
import datetime
import sys



#COM number file read for windows

DEV = (find_usb_device())[0]
#print(DEV)

class Battery(Enum):
    """
    毎回のレスポンスで帰ってくるバッテリー残量を表す列挙体。
    バッテリー情報取得要求で返ってくる返値とは別。
    """
    NG            = 0b000
    LOW           = 0b001
    HALF          = 0b011
    NO_BATTERY    = 0b100
    CHARGING_LOW  = 0b101
    CHARGING_HALF = 0b110
    CHARGING_HIGH = 0b111

class Backdoor(Enum):
    """
    チェキのバックカバー（カセットのふた）が開いているかをあらわす列挙体
    """
    CLOSE  = 0
    OPEN   = 1

class ErrorStatus(IntEnum):
    """
    エラー状態を表す列挙体
    """
    EncoderError  = 0b0001
    PISensorError = 0b0010
    MechanicError = 0b0100
    DecodeError   = 0b1000

class InstaxDriver():
    """
    Instax通信仕様書の実装。USBとWifiはそれぞれサブクラス化して使用する。
    """

    def __init__(self):
        self.transfer_size = None

    def put(self, bytecode):
        """
        PCからInstaxへパケットを送信するメソッド。
        サブクラスで実装する。
        """
        raise NotImplementedError()

    def get(self, nbytes):
        """
        InstaxからPCへパケットを受信するメソッド。
        サブクラスで実装する。
        """
        raise NotImplementedError()

    def check_sum(self, _bytes):
        """
        バイト列(_bytes)からチェックサムを計算する。
        """
        return 0xffff & sum(struct.unpack(">%dB" % len(_bytes), _bytes))

    def check_response(self, _bytes):
        """
        レスポンスのバイト列(s)が正しく通信できているかをチェックサム（最後4-byte : s[:-4]）
        で確認して結果をブール(True, False)で返す。
        """
        ck_sum, = struct.unpack('>H', _bytes[-4:-2])
        return (self.check_sum(_bytes[:-4]) + ck_sum) == 0xffff

    def close(self):
        """
        通信を終了する。サブクラスで実装されている。
        """
        raise NotImplementedError()

    @retry(tries=3, delay=0.1)     ###Deff
    def send_cmd(self, service_id, data=b''):
        """
        PCからInstaxへコマンドを送信する。

        Parameters
        ----------
        service_id : int
            Instax仕様書で定義されているSID
        data : byte
            データのバイト列
        """
        frm_length = len(data) + 16
        byte_codes = struct.pack('>BBHiHH',
                                 0x24,      # Header
                                 service_id, # Service ID
                                 frm_length, # frame length
                                 0,         # SndID
                                 1111,    # = 0x0457,    # default Password
                                 0,
                                )
        byte_codes = byte_codes + data
        ck_sum = 0xffff - self.check_sum(byte_codes)
        self.put(byte_codes + struct.pack(">HBB", ck_sum, 0x0d, 0x0a))
        resp = self.read_response()    ###Deff
        return resp

    def set_autosleep(self, is_autosleep = True):
        """
        オートスリープを設定するかどうか。
        オートスリープになっていると自動的にInstaxがオフになる。
        """
        if is_autosleep:
            auto_sleep_flag = 1
        else:
            auto_sleep_flag = 2
        return self.send_cmd(0xB8, struct.pack(">bbbbHHHH", auto_sleep_flag, 0, 0, 0, 0, 0, 0, 0))

    def get_information(self):
        """
        Instaxから情報を取得する。
        """
        info, resp_ok, res_code = self.send_cmd(0xC1) #Getting information
        return (info, resp_ok, res_code)



    def get_battery_status(self):
        if self.status is None:
            self.get_information()
        battery_status = ((self.status >> 4) & 0b111)
        return Battery(battery_status)

    def get_backdoor_status(self):
        """
        バックドア（カセットのふた）の状態を返す。
        Backdoor.OPEN  : 開いた状態
        Backdoor.CLOSE : 閉じた状態
        """
        if self.status is None:
            self.get_information()
        battery_status = ((self.status >> 7) & 0b1)
        return Backdoor(battery_status)

    def get_filmpack_status(self):
        if self.status is None:
            self.get_information()
        filmpack_status = self.status & 0b1111
        if filmpack_status < 11:
            return filmpack_status# Number of films
        else:
            return -1# No filmpack

    def get_error_status(self):
        if self.status is None:
            self.get_information()
        error_status = ((self.status >> 12) & 0b1111)
        errors = []
        if (ErrorStatus.EncoderError & error_status) != 0:
            errors.append(ErrorStatus.EncoderError)
        if (ErrorStatus.PISensorError & error_status) != 0:
            errors.append(ErrorStatus.PISensorError)
        if (ErrorStatus.MechanicError & error_status) != 0:
            errors.append(ErrorStatus.MechanicError)
        if (ErrorStatus.DecodeError & error_status) != 0:
            errors.append(ErrorStatus.DecodeError)
        return errors

    def print_img(self, img):
        self.print_pre_img(img)   ###Deff
        self.print_main_img()   ###Deff

    def print_pre_img(self, img):
        # logging.debug('C2=%s', self.send_cmd(0xC2)) # Get Machine name -> SP-2
        # logging.debug('C0=%s', self.send_cmd(0xC0)) #Getting FIRM&FPGA Version
        # logging.debug('4F=%s', self.send_cmd(0x4F)) #Getting parameter size
        # logging.debug('C1=%s', self.send_cmd(0xC1)) #Getting information
        # logging.debug('B3=%s', self.send_cmd(0xB3, struct.pack('>BBBB', 1, 0, 0, 0)))#Processing Lock or UnLock

        logging.debug('50=%s', self.send_cmd(0x50)) #Resetimage
        # Start Image Download


        ###ADD
        _, _, _ = self.send_cmd(0x51, struct.pack('>BBiiBB',
                                                  0x10,          # 0x01:BMP, 0x02:JPG, 0x10:Line
                                                  0,
                                                  600 * 800 * 3, # picSize
                                                  0,
                                                  0,             # fixed
                                                  0,             # fixed
                                                  ))
        self.send_img(img)

        logging.debug('53=%s', self.send_cmd(0x53)) #Imaging download exit

    def print_main_img(self):

        ###ADD
        logging.debug('B0=%s', self.send_cmd(0xB0)) #Printing start
        logging.debug('B3=%s', self.send_cmd(0xB3, struct.pack(">BBBB", 0x0, 0, 0, 0))) #Processing Lock or UnLock
        



    def send_img(self, img):

        ###Alter
        #image load
        data, number = self.load_image(img)

        #data transfer
        i = 0
        while i < number:
            #Image Transfer(down)
            status, resp_ok, resCode = self.send_cmd(0x52, struct.pack('>i', i) + data[i])
            logging.debug((status, resp_ok, resCode))
            if not resp_ok:
                # retry sending not
                logging.warning("Check sum mismatched!!")
            elif resCode != 0:
                # retry sending
                logging.warning("Response code error!! : %d", resCode)
            else:
                i += 1

    def load_image(self, img, image_size=600*800*3):
        h, w, _ = np.shape(img)
        img = img[::-1, :] #Inverted Image

        #RGB -> RAW format
        convert_data = []
        for j in range(h):
            convert_data.append([img[j,0:w,i] for i in range(3)])
        data1 = np.array(convert_data).reshape(-1,)

        number = int(image_size / self.transfer_size)

        #convert to transfer_size units
        data = []
        for i in range(0, number):
    #        data.append(data1.astype('d').to_string())
            data.append(struct.pack(">%dB" % self.transfer_size,
                                    *data1[i*self.transfer_size:(i+1)*self.transfer_size]))

        return data, number

    RESPONSE = {
        0x3f : lambda data: struct.unpack(">%ds" % len(data), data), # FIXME : Not implemented yet
        0x40 : lambda data: struct.unpack(">xxxB%ds" % len(data) - 4, data), # FIXME: not tested
        0x4E : lambda data: struct.unpack(">xxH", data), # FIXME: not tested
        0x4F : lambda data: struct.unpack(">HHHHxxxxHBxIxxxxxxxx", data), # FIXME: not tested
        0x51 : lambda data: struct.unpack(">xxH", data), # FIXME: not tested
        0x52 : lambda data: struct.unpack(">i", data),
        0x54 : lambda data: struct.unpack(">BBIIH", data), # FIXME: not tested
        0x55 : lambda data: struct.unpack(">II", data), # FIXME: not tested
        0x73 : lambda data: struct.unpack(">xxxB", data), # FIXME: not tested
        0x74 : lambda data: struct.unpack(">xxxB", data), # FIXME: not tested
        0x75 : lambda data: struct.unpack(">xxH", data), # FIXME: not tested
        0x76 : lambda data: struct.unpack(">xxxB%ds" % len(data) - 4, data), # FIXME: not tested
        0x77 : lambda data: struct.unpack(">I", data), # FIXME: not tested
        0xc1 : lambda data: struct.unpack("IHHIxBxx", data),
        0xc2 : lambda data: struct.unpack(">%ds" % len(data), data),
        0xc5 : lambda data: struct.unpack(">xxxb%dc"),
        0xb0 : lambda data: struct.unpack(">i", data)
    }
    def read_response(self):
        """
        Instaxからレスポンスを受け取り、数値を取り出して返す。
        """
        resp = self.get(16)
        if len(resp) != 16: raise Exception("Response too short!! : %d" % len(resp))   #Deff
        # logging.debug("RESP:%s", resp)
        _, sid, length, resCode, status = struct.unpack('>BBHxxxxxxxxBxH', resp)
        self.status = status
        resp += self.get(length - 16)
        resp_ok = self.check_response(resp)
        if len(resp) != length:     #Deff
            raise Exception("Response too short!! : %d" % len(resp))
        data = resp[16:-4]
        if not sid in self.RESPONSE:
            return (), resp_ok, resCode
        else:
            return self.RESPONSE[sid](data), resp_ok, resCode

    def remaining_number_of_sheets(self):
        """
        残り枚数を返す
        """
        return 0b1111 & self.status



class WifiDriver(InstaxDriver):

    def __init__(   self,
                    host="192.168.0.251", #Instax IP
                    port=8080             #Instax Port
                ):
#        super(WifiDriver, self).__init__()
        import socket
        self.transfer_size = 60000
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client.connect((host, port))

    def get(self, nbytes):
        return self.client.recv(nbytes)

    def put(self, bytecode):
        self.client.send(bytecode)

    def close(self):
        self.client.close()

class USBDriver(InstaxDriver):

    def __init__(self, dev=DEV):
#        super(USBDriver, self).__init__()
        import serial

        ###Alter
        self.transfer_size = 1800
        self.client = serial.Serial(port=dev,
                                    baudrate=115200,
                                    parity=serial.PARITY_NONE,
                                    bytesize=serial.EIGHTBITS,
                                    stopbits=serial.STOPBITS_ONE,
                                    timeout=0.2,
                                    writeTimeout=5.0,
                                    xonxoff=False)
        # USB needs maintainance mode -> 0xBE
        logging.debug(self.send_cmd(0xBE))

    def put(self, bytecode):
        self.client.write(bytecode)

    def get(self, nbytes):
        return self.client.read(nbytes)

    def close(self):
        self.client.close()



"""New for Link - Start Point"""
class InstaxDriverForLink():
    """
    Instax通信仕様書の実装。USBの箇所はサブクラス化。
    """

    def __init__(self):
        self.transfer_size = None

    def put(self, bytecode):
        """
        PCからInstaxへパケットを送信するメソッド。
        サブクラスで実装する。
        """
        raise NotImplementedError()

    def get(self, nbytes):
        """
        InstaxからPCへパケットを受信するメソッド。
        サブクラスで実装する。
        """
        raise NotImplementedError()

    def check_sum(self, _bytes):
        """
        バイト列(_bytes)からチェックサムを計算する。
        """
        return 0xffff & sum(struct.unpack(">%dB" % len(_bytes), _bytes))

    def check_response(self, _bytes):
        """
        レスポンスのバイト列(s)が正しく通信できているかをチェックサム（最後4-byte : s[:-4]）
        で確認して結果をブール(True, False)で返す。
        """
        ck_sum, = struct.unpack('>H', _bytes[-4:-2])
        return (self.check_sum(_bytes[:-4]) + ck_sum) == 0xffff

    def close(self):
        """
        通信を終了する。サブクラスで実装されている。
        """
        raise NotImplementedError()

    @retry(tries=3, delay=0.1) 
    def send_cmd(self, service_id, data=b''):
        """
        PCからInstaxへコマンドを送信する。

        Parameters
        ----------
        service_id : int
            Instax仕様書で定義されているSID
        data : byte
            データのバイト列
        """
        frm_length = len(data) + 16
        byte_codes = struct.pack('>BBHiHH',
                                 0x24,      # Header
                                 service_id, # Service ID
                                 frm_length, # frame length
                                 0,         # SndID
                                 1111,    # = 0x0457,    # default Password
                                 0,
                                )
        byte_codes = byte_codes + data
        ck_sum = 0xffff - self.check_sum(byte_codes)
        self.put(byte_codes + struct.pack(">HBB", ck_sum, 0x0d, 0x0a))
        return self.read_response()

    def set_autosleep(self, is_autosleep = True):
        """
        オートスリープを設定するかどうか。
        オートスリープになっていると自動的にInstaxがオフになる。
        """
        if is_autosleep:
            auto_sleep_flag = 1
        else:
            auto_sleep_flag = 2
        return self.send_cmd(0xB8, struct.pack(">bbbbHHHH", auto_sleep_flag, 0, 0, 0, 0, 0, 0, 0))

    def get_information(self):
        """
        Instaxから情報を取得する。
        """
        info, resp_ok, res_code = self.send_cmd(0xC1) #Getting information
        return (info, resp_ok, res_code)

    def get_instax_ID(self):
        """
        """
        info, resp_ok, res_code = self.send_cmd(0xC5, struct.pack(">xxxb", 0)) #Getting information
        return (info, resp_ok, res_code)

    def get_battery_status(self):
        if self.status is None:
            self.get_information()
        battery_status = ((self.status >> 4) & 0b111)
        return Battery(battery_status)

    def get_backdoor_status(self):
        """
        バックドア（カセットのふた）の状態を返す。
        Backdoor.OPEN  : 開いた状態
        Backdoor.CLOSE : 閉じた状態
        """
        if self.status is None:
            self.get_information()
        battery_status = ((self.status >> 7) & 0b1)
        return Backdoor(battery_status)

    def get_filmpack_status(self):
        if self.status is None:
            self.get_information()
        filmpack_status = self.status & 0b1111
        if filmpack_status < 11:
            return filmpack_status# Number of films
        else:
            return -1# No filmpack

    def get_error_status(self):
        if self.status is None:
            self.get_information()
        error_status = ((self.status >> 12) & 0b1111)
        errors = []
        if (ErrorStatus.EncoderError & error_status) != 0:
            errors.append(ErrorStatus.EncoderError)
        if (ErrorStatus.PISensorError & error_status) != 0:
            errors.append(ErrorStatus.PISensorError)
        if (ErrorStatus.MechanicError & error_status) != 0:
            errors.append(ErrorStatus.MechanicError)
        if (ErrorStatus.DecodeError & error_status) != 0:
            errors.append(ErrorStatus.DecodeError)
        return errors

    def print_img(self, img):
        self.print_pre_img(img)
        self.print_main_img()

    def print_pre_img(self, img):   ###Alter###
        # logging.debug('C2=%s', self.send_cmd(0xC2)) # Get Machine name -> SP-2
        # logging.debug('C0=%s', self.send_cmd(0xC0)) #Getting FIRM&FPGA Version
        # logging.debug('4F=%s', self.send_cmd(0x4F)) #Getting parameter size
        # logging.debug('C1=%s', self.send_cmd(0xC1)) #Getting information
        # logging.debug('B3=%s', self.send_cmd(0xB3, struct.pack('>BBBB', 1, 0, 0, 0)))#Processing Lock or UnLock

        logging.debug('50=%s', self.send_cmd(0x50)) #Resetimage
        # Start Image Download

        #encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #_, img_enc = cv2.imencode('.jpg', img, encode_param)
        res_values = self.send_cmd(0x4F)
        #print(res_values[0][6])
        comp_value = 100
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), comp_value]
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        _, img_enc = cv2.imencode('.jpg', img2, encode_param)
        while res_values[0][6] < len(img_enc):
            #print(len(img_enc), comp_value)
            comp_value -= 1
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), comp_value]
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            _, img_enc = cv2.imencode('.jpg', img2, encode_param)            
        #print(len(img_enc), comp_value)

        value, _, _ = self.send_cmd(0x51, struct.pack('>BBiiBB',
                                                  0x02,          # 0x01:BMP, 0x02:JPG, 0x10:Line
                                                  0,
                                                  len(img_enc),  # picSize 600 * 800 * 3
                                                  0,
                                                  0,             # fixed
                                                  0,             # fixed
                                                ))
        self.transfer_size = value[0]
        self.send_img(img_enc)
        logging.debug('53=%s', self.send_cmd(0x53)) #Imaging download exit

    def print_main_img(self):   ###Alter###
        logging.debug('C0=%s', self.send_cmd(0xC0)) 
        logging.debug('B0=%s', self.send_cmd(0xB0)) #Printing start
        logging.debug('C3=%s', self.send_cmd(0xC3)) 
        _, _, resCode = self.send_cmd(0xC3)
        while resCode != 0:
            _, _, resCode = self.send_cmd(0xC3)
        logging.debug('B3=%s', self.send_cmd(0xB3, struct.pack(">BBBB", 0x0, 0, 0, 0))) #Processing Lock or UnLock
        
    def send_img(self, img):
        #image load
        data, number = self.load_image(img)
        #data transfer
        i = 0
        while i < number:
            #Image Transfer(down)
            status, resp_ok, resCode = self.send_cmd(0x52, struct.pack('>i', i) + data[i])
            logging.debug((status, resp_ok, resCode))
            if not resp_ok:
                # retry sending not
                logging.warning("Check sum mismatched!!")
            elif resCode != 0:
                # retry sending
                logging.warning("Response code error!! : %d", resCode)
            else:
                i += 1

    def load_image(self, img):   ###Alter###
        convert_data = []
        for j in range(len(img)):
            convert_data.append(int(img[j]))
        data = []
        number = int(len(img)/self.transfer_size)
        for i in range(0,number+1):
            count = len(convert_data[i*self.transfer_size:(i+1)*self.transfer_size])
            if count == self.transfer_size:
                data1 = struct.pack(">%dB" % self.transfer_size, *convert_data[i*self.transfer_size:(i+1)*self.transfer_size])
                data.append(data1)
            else:
                data1 = struct.pack(">%dB" % count, *convert_data[i*self.transfer_size:i*self.transfer_size+count])
                zero_list = np.zeros(self.transfer_size-count).astype(int)
                padding = struct.pack("%dB" % (self.transfer_size-count), *zero_list)
                data1 = data1 + padding
                data.append(data1)
                number = number + 1
        return data, number

    RESPONSE = {
        0x3f : lambda data: struct.unpack(">%ds" % len(data), data), # FIXME : Not implemented yet
        0x40 : lambda data: struct.unpack(">xxxB%ds" % len(data) - 4, data), # FIXME: not tested
        0x4E : lambda data: struct.unpack(">xxH", data), # FIXME: not tested
        0x4F : lambda data: struct.unpack(">HHHHxxxxHBxIxxxxxxxx", data), # FIXME: not tested
        0x51 : lambda data: struct.unpack(">xxH", data), # FIXME: not tested
        0x52 : lambda data: struct.unpack(">i", data),
        0x54 : lambda data: struct.unpack(">BBIIH", data), # FIXME: not tested
        0x55 : lambda data: struct.unpack(">II", data), # FIXME: not tested
        0x73 : lambda data: struct.unpack(">xxxB", data), # FIXME: not tested
        0x74 : lambda data: struct.unpack(">xxxB", data), # FIXME: not tested
        0x75 : lambda data: struct.unpack(">xxH", data), # FIXME: not tested
        0x76 : lambda data: struct.unpack(">xxxB%ds" % len(data) - 4, data), # FIXME: not tested
        0x77 : lambda data: struct.unpack(">I", data), # FIXME: not tested
        0xc1 : lambda data: struct.unpack("IHHIxBxx", data),
        0xc2 : lambda data: struct.unpack(">%ds" % len(data), data),
        0xc5 : lambda data: struct.unpack(">xxxb%ds" % (len(data) - 4), data),

        0xb0 : lambda data: struct.unpack(">i", data)
    }

    def read_response(self):
        """
        Instaxからレスポンスを受け取り、数値を取り出して返す。
        """
        resp = self.get(16)
        if len(resp) != 16: raise Exception("Response too short!! : %d" % len(resp))
        # logging.debug("RESP:%s", resp)
        _, sid, length, resCode, status = struct.unpack('>BBHxxxxxxxxBxH', resp)
        self.status = status
        resp += self.get(length - 16)
        resp_ok = self.check_response(resp)
        if len(resp) != length:
            raise Exception("Response too short!! : %d" % len(resp))
        data = resp[16:-4]
        if not sid in self.RESPONSE:
            return (), resp_ok, resCode
        else:
            return self.RESPONSE[sid](data), resp_ok, resCode

    def remaining_number_of_sheets(self):
        """
        残り枚数を返す
        """
        return 0b1111 & self.status

class LinkDriver(InstaxDriverForLink):

    def __init__(self, dev=DEV):
#        super(USBDriver, self).__init__()
        import serial

###DELETE        self.transfer_size = 1800
        self.client = serial.Serial(port=dev,
                                    baudrate=115200,
                                    parity=serial.PARITY_NONE,
                                    bytesize=serial.EIGHTBITS,
                                    stopbits=serial.STOPBITS_ONE,
                                    timeout=0.2,
                                    writeTimeout=5.0,
                                    xonxoff=False)
        # USB needs maintainance mode -> 0xBE
        logging.debug(self.send_cmd(0xBE))

    def put(self, bytecode):
        self.client.write(bytecode)

    def get(self, nbytes):
        return self.client.read(nbytes)

    def close(self):
        self.client.close()
"""New for Link - End Point"""


def print_instax(img, mode, dev=DEV):
    print_instax_pre(img, mode, dev=dev)
    remain_num = print_instax_main(mode, dev=dev)
    return remain_num

def auto_sleep_status(mode, dev=DEV, state=True):
    #check license 
    if check_license(dev=dev) is False:
        return "license error"

    #command test
    if mode == 'wifi':
        driver = WifiDriver()
    elif mode == 'usb':
        driver = USBDriver(dev=dev)
    elif mode == 'link':   ###ADD###
        driver = LinkDriver(dev=dev)

    driver.set_autosleep(state)
    driver.close()


def print_instax_pre(img, mode, dev=DEV):
    #check license 
    if check_license(dev=dev) is False:
        return "license error"

     #command test
    if mode == 'wifi':
        driver = WifiDriver()
    elif mode == 'usb':
        driver = USBDriver(dev=dev)
    elif mode == 'link':   ###ADD###
        driver = LinkDriver(dev=dev)

    driver.set_autosleep(False)
    # print(driver.get_battery_status())
    # print(driver.get_backdoor_status())
    # print(driver.get_filmpack_status())
    # print(driver.get_error_status())
    # exit()

    print("image data transfer start")
    driver.print_pre_img(img)
    print("image data transfer end")
    
    driver.close()

def print_instax_main(mode, dev=DEV):
    #check license 
    if check_license(dev=dev) is False:
        return "license error"

    #command test
    if mode == 'wifi':
        driver = WifiDriver()
    elif mode == 'usb':
        driver = USBDriver(dev=dev)
    elif mode == 'link':   ###ADD###
        driver = LinkDriver(dev=dev)

    remain_num = driver.remaining_number_of_sheets()

    #print('Remaining number of sheets is ', remain_num)
    if remain_num == 0:
        print('Set new cartrige ! Remaining number of sheets is ', remain_num)
        driver.close()
        return

    driver.print_main_img()
    driver.close()

    return remain_num - 1 

def get_instax_ID(mode, dev=DEV):
    #command test
    if mode == 'wifi':
        driver = WifiDriver()
    elif mode == 'usb':
        driver = USBDriver(dev=dev)
    elif mode == 'link':   ###ADD###
        driver = LinkDriver(dev=dev)

    (_, iid), _, _ = driver.get_instax_ID()
    
    driver.close()
    return iid.decode('utf-8')

def get_print_number(dev=DEV, mode='wifi'):
    #check license 
    if check_license(dev=dev) is False:
        return "license error"

    #command test
    if mode == 'wifi':
        driver = WifiDriver()
    elif mode == 'usb':
        driver = USBDriver(dev=dev)
    elif mode == 'link':   ###ADD###
        driver = LinkDriver(dev=dev)

    if driver.get_backdoor_status() == Backdoor.CLOSE:
        remain_num = driver.remaining_number_of_sheets()
        driver.close()
        return remain_num
    else:
        driver.close()
        return

def check_license(dev=DEV, path="./license", max_file_number=10):

    file_lists = glob.glob(path+'/*.lic')
    flag = False

    if len(file_lists) <= max_file_number:
        for file_path in file_lists:
            if check_license_file(file_path, dev=dev) is True:
                flag = True
    else:
        print("license error!")
        print("The number of license files included in the folder (./license) should be 10 or less.\n"+
              "Check your license files at the folder(./license) and Instax printer.")
        input()
        return False
        
    if flag is False:
        print("license error!")
        print("The license and the Instax printer do not match or the license has expired.\n"+
              "Check your license files at the folder(./license) and Instax printer.")
        input()
        return False
    return True

def check_license_file(path_w, dev=DEV):
    #file read
    with open(path_w, mode='rb') as f:
        ciphertext = f.read()
        f.close()

    #decode message
    private_key2 = key_load("./pem/private2.pem")
    message = decode_cipher(ciphertext, private_key2)
    serial_number = message.split()[0]
    time_limit = message.split()[1]

    time_limit = datetime.datetime.strptime(time_limit, '%Y-%m-%d')
    now_time = datetime.datetime.now()

    if now_time > time_limit:
        return False

    if serial_number != get_instax_ID('link', dev=dev):
        return False

    return True


def main():
    import util.image_processing_a as im_pro
    """
    デバッグのためのメイン関数
    """
    # start =　time.time()
    logging.basicConfig(filename="instax_print.log", level=logging.DEBUG)

    #img = cv2.imread("./target_files/kurin1.jpg")
    #img_f = cv2.imread("./frame/temp_GoodDesignAward.png",-1)
    #img = im_pro.img_process(img0, img_f)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   

    #import util.affine as af
    #img = af.processing(img) #change to Instax format 

    #print_instax(img, 'link') #print image to Instax by link
    DEV = (find_usb_device())[1]
    print(DEV)
    print(get_instax_ID('link', dev=DEV))
    auto_sleep_status('link', dev=DEV, state=False)
    print(get_print_number(dev=DEV, mode='link'))
    # print(time.time() - start)

if __name__ == '__main__':
    main()
