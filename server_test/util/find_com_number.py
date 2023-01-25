# find_com_number.py
# coding by Shinichiro Sonoda
# Nov. 8th 2020

import win32com.client
import sys

wmi = win32com.client.GetObject("winmgmts:")

def find_usb_device(text="VID_04CB&PID_5019"):
    count = 0
    devices =[]
    for usb in wmi.InstancesOf("win32_SerialPort"):
        if text in usb.PNPDeviceID:
            com_number = usb.DeviceID
            devices.append(com_number)
            count += 1
    if count == 0:
        print("The USB-connected Instax link was not found.")
        return
    elif count >= 1:
        return devices
    else:
        print("The USB-connected error.")
        print('Please push Enter key.')
        input()
        sys.exit()

if __name__ == '__main__':
    print(find_usb_device())
