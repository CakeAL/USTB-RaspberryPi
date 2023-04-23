import RPi.GPIO as GPIO
import time

makerobo_VibratePin = 11
makerobo_Rpin = 12
makerobo_Gpin = 13

clb_tmp = 0


def makerobo_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(makerobo_Rpin, GPIO.OUT)
    GPIO.setup(makerobo_Gpin, GPIO.OUT)
    GPIO.setup(makerobo_VibratePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def double_colorLED(x):
    if x == 0:
        GPIO.output(makerobo_Rpin, 1)
        GPIO.output(makerobo_Gpin, 0)
    if x == 1:
        GPIO.output(makerobo_Rpin, 0)
        GPIO.output(makerobo_Gpin, 1)


def makerobo_Print(x):
    global clb_tmp
    if x != clb_tmp:
        if x == 0:
            print('*****************')
            print('* Makerobo    ON*')
            print('*****************')
        if x == 1:
            print('*****************')
            print('* OFF  Makerobo *')
            print('*****************')
    clb_tmp = x

def makerobo_loop():
    clb_state = 0
    while True:
        if GPIO.input(makerobo_VibratePin) == 1:
            clb_state = clb_state + 1
            if clb_state > 1:
                clb_state = 0
            double_colorLED(clb_state)
            makerobo_Print(clb_state)
            time.sleep(1)


def makerobo_destory():
    GPIO.output(makerobo_Rpin, GPIO.HIGH)
    GPIO.output(makerobo_Gpin, GPIO.HIGH)
    GPIO.cleanup()


if __name__ == '__main__':
    makerobo_setup()
    try:
        makerobo_loop()
    except KeyboardInterrupt:
        makerobo_destory()