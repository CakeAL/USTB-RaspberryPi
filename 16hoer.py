import RPi.GPIO as GPIO
import PCF8591 as ADC
import time


def makerobo_setup():
    ADC.setup(0x48)


def makerobo_Print(x):
    if x == 0:
        print('')
        print('**************')
        print('*  No Magnet *')
        print('**************')
        print('')
    if x == 1:
        print('')
        print('****************')
        print('* Magnet North *')
        print('****************')
        print('')
    if x == -1:
        print('')
        print('****************')
        print('* Magnet South *')
        print('****************')
        print('')


def makerobo_loop():
    makerobo_status = 0
    while True:
        makerobo_res = ADC.read(0)
        print('Current intensity of magnetic field:', makerobo_res)
        if 5 > makerobo_res - 133 > -5:
            makerobo_tmp = 0
        if makerobo_res < 128:
            makerobo_tmp = -1
        if makerobo_res > 138:
            makerobo_tmp = 1
        if makerobo_tmp != makerobo_status:
            makerobo_Print(makerobo_tmp)
            makerobo_status = makerobo_tmp
        time.sleep(0.2)


if __name__ == '__main__':
    makerobo_setup()
    makerobo_loop()
