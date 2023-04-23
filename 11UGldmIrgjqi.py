import RPi.GPIO as GPIO

makerobo_PIpin = 11
makerobo_Rpin = 12
makerobo_Gpin = 13

def makerobo_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(makerobo_Rpin, GPIO.OUT)
    GPIO.setup(makerobo_Gpin, GPIO.OUT)
    GPIO.setup(makerobo_PIpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(makerobo_PIpin, GPIO.BOTH, callback=makerobo_detect, bouncetime=10)

def double_colorLED(x):
    if x == 0:
        GPIO.output(makerobo_Rpin, 1)
        GPIO.output(makerobo_Gpin, 0)
    if x == 1:
        GPIO.output(makerobo_Rpin, 0)
        GPIO.output(makerobo_Gpin, 1)


def makerobo_Print(x):
    if x == 0:
        print('**************************************')
        print('*     Makerobo Light was blocked     *')
        print('**************************************')


def makerobo_detect(chn):
    #print(GPIO.input(makerobo_PIpin))
    double_colorLED(GPIO.input(makerobo_PIpin))
    makerobo_Print(GPIO.input(makerobo_PIpin))


def loop():
    while True:
        #double_colorLED(1)
        pass

def destroy():
    GPIO.output(makerobo_Gpin, GPIO.HIGH)
    GPIO.output(makerobo_Rpin, GPIO.HIGH)
    GPIO.cleanup()


if __name__ == '__main__':
    makerobo_setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()