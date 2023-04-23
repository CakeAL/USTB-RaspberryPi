import PCF8591 as ADC
import time


def makerobo_setup():
    ADC.setup(0x48)
    global makerobo_state


def makerobo_direction():
    state = ['home', 'up', 'down', 'left', 'right', 'pressed']
    i = 0
    if ADC.read(0) <= 30:
        i = 1
    if ADC.read(0) >= 225:
        i = 2
    if ADC.read(1) >= 225:
        i = 4
    if ADC.read(1) <= 30:
        i = 3
    if ADC.read(2) == 0 and ADC.read(0) > 35 and ADC.read(0) < 220 and ADC.read(1) > 35 and ADC.read(1) < 220:
        i = 5
    if ADC.read(0) - 125 < 15 and ADC.read(0) - 125 > -15 and ADC.read(1) - 125 < 15 and ADC.read(
            1) - 125 > -15 and ADC.read(2) == 255:
        i = 0
    return state[i]


def makerobo_loop():
    makerobo_status = ''
    while True:
        makerobo_tmp = makerobo_direction()
        if makerobo_tmp is not None and makerobo_tmp != makerobo_status:
            print(makerobo_tmp)
            makerobo_status = makerobo_tmp


def destroy():
    pass


if __name__ == '__main__':
    makerobo_setup()
    try:
        makerobo_loop()
    except KeyboardInterrupt:
        destroy()
