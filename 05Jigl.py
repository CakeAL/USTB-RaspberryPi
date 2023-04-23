import RPi.GPIO as GPIO
import time
makerobo_LaserPin = 11
def makerobo_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(makerobo_LaserPin,GPIO.OUT)
    GPIO.output(makerobo_LaserPin,GPIO.LOW)
def makerobo_loop():
    while True:
        GPIO.output(makerobo_LaserPin,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(makerobo_LaserPin,GPIO.LOW)
def makerobo_destroy():
    GPIO.output(makerobo_LaserPin,GPIO.LOW)
    GPIO.cleanup()
if __name__ == '__main__':
    makerobo_setup()
    try:
        makerobo_loop()
    except KeyboardInterrupt:
        makerobo_destroy()
    
