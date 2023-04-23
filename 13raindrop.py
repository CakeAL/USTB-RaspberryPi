import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

makerobo_DO = 17
GPIO.setmode(GPIO.BCM)


def makerobo_setup():
    ADC.setup(0x48)
    GPIO.setup(makerobo_DO, GPIO.IN)


def makerobo_Print(x):
    if x == 1:
        print("")
        print("************************")
        print("* makerobo Not raining *")
        print("************************")
        print("")
    if x == 0:
        print("")
        print("************************")
        print("*  makerobo Raining!!  *")
        print("************************")
        print("")


def makerobo_loop():
    makerobo_status = 1
    while True:
        print(ADC.read(0))
        makerobo_tmp = GPIO.input(makerobo_DO)
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