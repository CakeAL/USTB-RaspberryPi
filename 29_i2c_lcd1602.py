import LCD1602
import time

def setup():
    LCD1602.init(0x27, 1)
    LCD1602.write(0, 0, "Greetings!!")
    LCD1602.write(1, 1, "WWW.WWWWWWW")
    time.sleep(2)


def loop():
    space = "..............."
    greetings = "Thank you for buying ZHIYU Sensor Kit For Rpi"
    greetings = space + greetings
    while True:
        tmp = greetings
        for i in range(0, len(greetings)):
            LCD1602.write(0, 0, tmp)
            tmp = tmp[1:]
            time.sleep(0.8)
            LCD1602.clear()


def destroy():
    pass

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()