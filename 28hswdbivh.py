import RPi.GPIO as GPIO

ObstaclePin = 11


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def loop():
    while True:
        if (0 == GPIO.input(ObstaclePin)):
            print(GPIO.input(ObstaclePin))
            print("Detected Barrier")


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()