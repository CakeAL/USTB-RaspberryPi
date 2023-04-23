import PCF8591 as ADC
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


def makerobo_setup():
    ADC.setup(0x48)


def makerobo_loop():
    makerobo_count = 0
    while True:
        makerobo_voiceValue = ADC.read(0)
        if makerobo_voiceValue:
            print("Sound Value:", makerobo_voiceValue)
            if makerobo_voiceValue < 80:
                print("Voice detected!", makerobo_count)
                makerobo_count += 1
            time.sleep(0.2)


if __name__ == '__main__':
    try:
        makerobo_setup()
        makerobo_loop()
    except KeyboardInterrupt:
        pass
