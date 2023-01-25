import util.instax_auto_sleep_status as ix_status

import util.affine as af
import cv2
import sys
import serial
import datetime
from util.log_file import log_file

try:
    import util.instax_print_usb3_link as ix
    message1 = ix.get_instax_ID('link') # instax SN
except serial.serialutil.SerialException as e:
    print("\n" + "Please confirm instax power switch.")
    print('Please push Enter key.')
    input()
    sys.exit()

# error log file
log_file_name='./log/check_instax.log'

# case3:demo instax auto sleep false
def instax_remain_num():
    # license check
    if ix.get_print_number(mode='link') == "license error":
        sys.exit()
    # printer check
    if ix.get_print_number(mode='link') == None:
        sys.exit()

    try:
        # set instax auto sleep false
        ix_status.set_status(False, mode="link")

        #print image to Instax link
        remain_num = ix.get_print_number(mode='link')
        print('Remaining number of sheets is ', remain_num)

        return remain_num

    except:
        dt_now = datetime.datetime.now()
        message = "error occur in " + str(file_name) + ' at ' + str(dt_now)
        print(message)
        log_file(message, log_file_name=log_file_name)

        import traceback
        except_str = traceback.format_exc()
        print(except_str)
        log_file(except_str, log_file_name=log_file_name)
        print('Please push Enter key.')
        input()


if __name__ == '__main__':
    instax_remain_num()
    print('Please push Enter key.')
    input()
