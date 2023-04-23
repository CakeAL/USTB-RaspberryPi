import PCF8591 as ADC
import time


def makerobo_setup():
    ADC.setup(0x48)


def makerobo_loop():
    makerobo_status = 1
    while True:
        print('Potentiometer Value:', ADC.read(0))
        makerobo_Value = ADC.read(0)
        makerobo_outvalue = map(makerobo_Value, 0, 255, 10, 255)
        ADC.write(makerobo_outvalue)
        time.sleep(0.2)


def destroy():
    ADC.write(0)


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


if __name__ == '__main__':
    try:
        makerobo_setup()
        makerobo_loop()
    except KeyboardInterrupt:
        destroy()