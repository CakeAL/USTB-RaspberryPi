import RPi.GPIO as GPIO
import PCF8591 as ADC
import time
import math

makerobo_DO = 17
GPIO.setmode(GPIO.BCM)


def makerobo_setup():
    ADC.setup(0x48)
    GPIO.setup(makerobo_DO, GPIO.IN)


def makerobo_Print(x):
    if x == 1:
        print('')
        print('***********')
        print('* Better~ *')
        print('***********')
        print('')
    if x == 0:
        print('')
        print('************')
        print('* Too Hot! *')
        print('************')
        print('')


def makerobo_loop():
    makerobo_status = 1
    makerobo_tmp = 1
    while True:
        makerobo_analogVal = ADC.read(0)
        makerobo_Vr = 5 * float(makerobo_analogVal) / 255
        makerobo_Rt = 10000 * makerobo_Vr / (5 - makerobo_Vr)
        makerobo_temp = 1/(((math.log(makerobo_Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
        makerobo_temp = makerobo_temp - 273.15
        print('temperature =', makerobo_temp, 'C')
        makerobo_tmp = GPIO.input(makerobo_DO)
        #print(makerobo_tmp)

        if makerobo_tmp != makerobo_status:
            makerobo_Print(makerobo_tmp)
            makerobo_status = makerobo_tmp
        time.sleep(0.2)


if __name__ == '__main__':
    try:
        makerobo_setup()
        makerobo_loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    makerobo_setup()
    makerobo_loop()
