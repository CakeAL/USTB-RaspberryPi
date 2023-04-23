import RPi.GPIO as GPIO

TouchPin = 11
Gpin = 12
Rpin = 13

tmp = 0

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Gpin, GPIO.OUT)
    GPIO.setup(Rpin, GPIO.OUT)
    GPIO.setup(TouchPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)


def Led(x):
    if x == 0:
        GPIO.output(Rpin, 1)
        GPIO.output(Gpin, 0)
    if x == 1:
        GPIO.output(Rpin, 0)
        GPIO.output(Gpin, 1)


def Print(x):
    global tmp
    if x != tmp:
        if x == 0:
            print("******")
            print("* ON *")
            print("******")
        if x == 1:
            print("*******")
            print("* OFF *")
            print("*******")
        tmp = x


def loop():
    while True:
        Led(GPIO.input(TouchPin))
        Print(GPIO.input(TouchPin))


def destroy():
    GPIO.output(Gpin, GPIO.HIGH)
    GPIO.output(Rpin, GPIO.HIGH)
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()