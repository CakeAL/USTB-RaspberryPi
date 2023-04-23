import RPi.GPIO as GPIO

makerobo_BtnPin = 11
makerobo_Rpin = 12
makerobo_Gpin = 13


def makerobo_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(makerobo_Rpin, GPIO.OUT)
    GPIO.setup(makerobo_Gpin, GPIO.OUT)
    GPIO.setup(makerobo_BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(makerobo_BtnPin, GPIO.BOTH, callback=makerobo_detect, bouncetime=200)


def double_colorLED(x):
    if x == 0:
        GPIO.output(makerobo_Rpin, 1)
        GPIO.output(makerobo_Gpin, 0)
    if x == 1:
        GPIO.output(makerobo_Rpin, 0)
        GPIO.output(makerobo_Gpin, 1)


def makerobo_Print(x):
    if x == 0:
        print('****************************************')
        print('* makerobo Raspberry Kit Button Pressed*')
        print('****************************************')


def makerobo_detect(chn):
    double_colorLED(GPIO.input(makerobo_BtnPin))
    makerobo_Print(GPIO.input(makerobo_BtnPin))


def makerobo_loop():
    while True:
        pass


def makerobo_destroy():
    GPIO.output(makerobo_Gpin, GPIO.LOW)
    GPIO.output(makerobo_Rpin, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    makerobo_setup()
    try:
        makerobo_loop()
    except KeyboardInterrupt:
        makerobo_destroy()
