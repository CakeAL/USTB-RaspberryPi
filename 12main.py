import PCF8591 as ADC


def makerobo_setup():
    ADC.setup(0x48)


def loop():
    while True:
        print(ADC.read(0))
        ADC.write(ADC.read(0))


def destory():
    ADC.write(0)


if __name__ == '__main__':
    try:
        makerobo_setup()
        loop()
    except KeyboardInterrupt:
        destory()
