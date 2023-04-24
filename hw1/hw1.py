"""
雨天控制行人红绿灯系统
用到模块 彩色LED，按键，PCF8591，雨滴传感器，有源蜂鸣器
彩色LED 用于控制红绿灯，基础设定每10s转换一次
按键 用于控制红绿灯，按下后无论状态是什么，重置为绿灯10s（如果是下雨状态为20s）
雨滴传感器用于检测是否下雨，如果检测到下雨，则留给行人通过的时间在刚才的基础上增加10s
有源蜂鸣器用于发出固定频率的声响，在绿灯时每1s发出0.2s的声音提醒视力障碍人群通过绿灯。
"""
import RPi.GPIO as GPIO
import PCF8591 as ADC
import time

# 管脚定义
RGB_R = 17
RGB_G = 18
RGB_B = 19
Btn = 20  # 按钮
Buzzer = 21  # 有源蜂鸣器
Raindrop = 22  # 雨滴传感器
# 其他全局变量
isRaining = 0  # 是否下雨
RedTime = 10  # 控制红灯默认10s
GreenTime = 10  # 控制绿灯默认10s
colors = {"R": 0x00ffff, "G": 0xff00ff, "B": 0xffff00}


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # 设置LED初始化
    global pins
    global p_R, p_G, p_B
    pins = {'pin_R': RGB_R, 'pin_G': RGB_G, 'pin_B': RGB_B}
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)
        GPIO.output(pins[i], GPIO.LOW)
    p_R = GPIO.PWM(pins['pin_R'], 2000)
    p_G = GPIO.PWM(pins['pin_G'], 1999)
    p_B = GPIO.PWM(pins['pin_B'], 5000)
    p_R.start(0)
    p_G.start(0)
    p_B.start(0)
    # 设置开关初始化
    GPIO.setup(Btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(Btn, GPIO.BOTH, callback=detect_btn, bouncetime=200)
    # 设置有源蜂鸣器初始化
    GPIO.setup(Buzzer, GPIO.OUT)
    GPIO.output(Buzzer, GPIO.LOW)  # 先关闭蜂鸣器
    # 设置雨滴传感器及PCF8591
    ADC.setup(0x48)
    GPIO.setup(Raindrop, GPIO.IN)


def makerobo_pwm_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# 颜色转换
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


led_color = 1  # 为1时是绿灯，为0时是红灯
cur_time = 10  # 本轮剩余时间
rain_status = 1  # 是否下雨，0表示下雨，1表示未下雨
# 按钮按下时触发
def detect_btn(chn):
    # todo 转变绿灯
    global cur_time, led_color
    print("有行人按下按钮，转变为绿灯。")
    cur_time = GreenTime
    led_color = 1


# 用于更改绿灯的时长
def change_green_time(x):
    global GreenTime
    if x == 1:
        print("现在开始不再下雨，绿灯时间改为10s")
        GreenTime = 10
    if x == 0:
        print("现在开始下雨，绿灯时间改为20s")
        GreenTime = 20


# 控制红绿灯
def control_led(cur_time_, led_color_):
    if led_color_ == 1:  # 绿灯时
        makerobo_set_Color(colors["G"])
        print("现在是绿灯，绿灯时间剩余:", cur_time_, "s")
        cur_time_ -= 1
        GPIO.setup(Buzzer, GPIO.LOW)  # 开启蜂鸣器0.2s
        time.sleep(0.3)
        GPIO.setup(Buzzer, GPIO.HIGH)  # 关闭蜂鸣器
        time.sleep(0.7)
    if led_color_ == 0:  # 红灯时
        GPIO.setup(Buzzer, GPIO.HIGH)  # 关闭蜂鸣器
        makerobo_set_Color(colors["R"])
        print("现在是红灯，红灯时间剩余:", cur_time_, "s")
        cur_time_ -= 1
        time.sleep(1.0)
    return cur_time_


def loop():
    global rain_status, cur_time, led_color
    while True:
        # print(ADC.read(0))
        temp_rain = GPIO.input(Raindrop)  # 接受Raindrop pin传进来的值
        # print(ADC.read(0))
        # print(temp_rain)
        if temp_rain != rain_status:  # 改变是否下雨状态
            change_green_time(temp_rain)
            rain_status = temp_rain
        if cur_time == 0:
            led_color = not led_color  # 当倒计时为0时，改变红绿灯状态
            if led_color == 1:  # 为绿灯时
                cur_time = GreenTime  # 设置本轮绿灯剩余时间
            else:
                cur_time = RedTime  # 设置本轮红灯剩余时间
        cur_time_ = control_led(cur_time, led_color)  # 进行控制红绿灯，每次1s
        if cur_time == GreenTime and cur_time_ < GreenTime - 1: #说明有行人按下了绿灯
            cur_time = GreenTime
        else:
            cur_time = cur_time_


def makerobo_destroy():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    #GPIO.setmode(GPIO.BOARD)
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)
        GPIO.output(pins[i], GPIO.LOW)
    GPIO.output(Buzzer, GPIO.HIGH)
    GPIO.cleanup()


if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        makerobo_destroy()
