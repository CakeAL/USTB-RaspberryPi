import RPi.GPIO as GPIO
import time

# colors = [0xFF0000,0x00FF00,0x0000FF,0xFFFF00,0xFF00FF,0x00FFFF]
colors = [0xFF0000, 0xFF7F00, 0xFFFF00, 0x00FF00, 0x00FFFF, 0x0000FF, 0x8B00FF]
makerobo_R = 11
makerobo_G = 12
makerobo_B = 13


# init
def makerobo_setup(Rpin, Gpin, Bpin):
    global pins
    global p_R, p_G, p_B
    pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)
        GPIO.output(pins[i], GPIO.LOW)
    p_R = GPIO.PWM(pins['pin_R'], 2000)
    p_G = GPIO.PWM(pins['pin_G'], 1999)
    p_B = GPIO.PWM(pins['pin_B'], 5000)
    p_R.start(0)
    p_G.start(0)
    p_B.start(0)


def makerobo_pwm_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def makerobo_off():
    GPIO.setmode(GPIO.BOARD)
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)
        GPIO.output(pins[i], GPIO.LOW)


def makerobo_set_Color(col):
    R_val = (col & 0xff0000) >> 16
    G_val = (col & 0x00ff00) >> 8
    B_val = (col & 0x0000ff) >> 0
    R_val = makerobo_pwm_map(R_val, 0, 255, 0, 100)
    G_val = makerobo_pwm_map(G_val, 0, 255, 0, 100)
    B_val = makerobo_pwm_map(B_val, 0, 255, 0, 100)
    p_R.ChangeDutyCycle(100 - R_val)
    p_G.ChangeDutyCycle(100 - G_val)
    p_B.ChangeDutyCycle(100 - B_val)


def makerobo_loop():
    while True:
        for col in colors:
            makerobo_set_Color(col)
            time.sleep(0.2)


def makerobo_destroy():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    makerobo_off()
    GPIO.cleanup()


if __name__ == "__main__":
    try:
        makerobo_setup(makerobo_R, makerobo_G, makerobo_B)
        makerobo_loop()
    except KeyboardInterrupt:
        makerobo_destroy()
