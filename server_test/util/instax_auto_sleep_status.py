# coding: utf-8
import util.instax_print_usb3_link as ix
import time

def set_status(state, DEV, mode="link"):

    flag = True
    count = 0

    while flag:
        try: 
            ix.auto_sleep_status(mode, dev=DEV, state=state)
            flag = False
        except:
            flag = True
            time.sleep(5)
            count += 1
            if count > 10:
                ix.auto_sleep_status(mode, dev=DEV, state=state)
                return count
    return count

if __name__ == '__main__':
    from util.find_com_number import find_usb_device # for windows

    DEV = (find_usb_device())[0]
    print(DEV)
    print(set_status(False, DEV))
