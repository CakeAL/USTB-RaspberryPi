import  RPi.GPIO as GPIO

TrackPin = 11
LedPin = 12


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LedPin, GPIO.OUT)
    GPIO.setup(TrackPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output(LedPin, GPIO.HIGH)


def loop():
    while True:
        if GPIO.input(TrackPin) == GPIO.LOW:
            print("White Line is detected.")
        else:
            print("...Black Line is detected.")
            GPIO.output(LedPin, GPIO.HIGH)


def destroy():
    GPIO.output(LedPin, GPIO.HIGH)
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()