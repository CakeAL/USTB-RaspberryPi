"""
作品背景：
在某些车流量不大的马路，可以让行人通过按钮来控制红绿灯使得等待时间减少，
同时运用雨滴传感器使得雨天时拥有更长的过马路时间。对于视力障碍人士，
可以通过有源蜂鸣器发出的声音信号来知晓红绿灯的状况从而辅助判断是否能够通过马路，
摄像头通过识别过路的汽车使得双色灯交替闪烁，提醒行人有车辆驶过。
用到组件:
彩色LED，按键，PCF8591，雨滴传感器，有源蜂鸣器 ，双色LED，摄像头
重要模块介绍：
彩色LED：用于控制红绿灯，基础设定每10s转换一次
按键：用于控制红绿灯，按下后无论状态是什么，重置为绿灯10s（如果是下雨状态为20s）
雨滴传感器(搭配PCF8591)：用于检测是否下雨，如果检测到下雨，则留给行人通过的时间在刚才的基础上增加10s
有源蜂鸣器：用于发出固定频率的声响，在绿灯时每1s发出0.3s的声音提醒视力障碍人群通过绿灯。
双色LED：用于检测到汽车后交替闪烁提醒行人。
摄像头：用于检测即将通过的汽车（简化的识别，通过检测色块来识别汽车）。
应用场景：
车流量不大，郊区的马路上，周围老龄化程度较深的社区。
"""
import RPi.GPIO as GPIO
import PCF8591 as ADC
import time
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import threading

# 管脚定义
RGB_R = 17
RGB_G = 18
RGB_B = 19
Btn = 20  # 按钮
Buzzer = 21  # 有源蜂鸣器
Raindrop = 22  # 雨滴传感器
DoubleLED_G = 23  # 双色LED的绿色
DoubleLED_R = 24
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
    # 设置双LED
    GPIO.setup(DoubleLED_G, GPIO.OUT)
    GPIO.setup(DoubleLED_R, GPIO.OUT)
    GPIO.setup(DoubleLED_R, GPIO.LOW)
    GPIO.setup(DoubleLED_G, GPIO.LOW)
    global DLED_R, DLED_G
    DLED_G = GPIO.PWM(DoubleLED_G, 2000)
    DLED_R = GPIO.PWM(DoubleLED_R, 2000)
    DLED_R.start(0)
    DLED_G.start(0)
    # 开启摄像头线程
    threading.Thread(target=colorDetectThread).start()


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
    # 转变绿灯
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
        if cur_time == GreenTime and cur_time_ < GreenTime - 1:  # 说明有行人按下了绿灯
            cur_time = GreenTime
        else:
            cur_time = cur_time_


def colorDetectThread():

    carDetect = 0  # 是否有车经过
    lastCarDetect = 0
    # 创建解释器
    ap = argparse.ArgumentParser()
    # 添加参数
    ap.add_argument("-v", "--video",
                    help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
                    help="max buffer size")
    # 解析参数
    args = vars(ap.parse_args())  # vars()将传递的函数从Namespace转换到dict
    colorLower = (0, 100, 100)
    colorUpper = (44, 255, 255)
    pts = deque(maxlen=args["buffer"])  # 设置最大值
    # if a video path was not supplied, grab the reference to the webcam
    if not args.get("video", False):
        camera = cv2.VideoCapture(0)
    else:
        camera = cv2.VideoCapture(args["video"])

    while True:
        # 设置初始状态
        makerobo_set_DoubleColor(0x00FF)
        carDetect = 0
        (grabbed, frame) = camera.read()
        if args.get("video") and not grabbed:
            break

        frame = imutils.resize(frame, width=600)  # 图像缩放，宽度600
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 转换到HSV
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)  # 图像腐蚀，迭代次数2
        mask = cv2.dilate(mask, None, iterations=2)  # 图像膨胀，迭代次数2
        # 检测外轮廓
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)  # 取轮廓面积最大值的点集
            ((x, y), radius) = cv2.minEnclosingCircle(c)  # 得到包含二维点集的最小圆
            M = cv2.moments(c)  # 求图像矩
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255, 2))
                cv2.circle(frame, center, 5, (0, 0, 255), -1)  # 画实心球
            # todo 用于添加闪烁代码
            makerobo_set_DoubleColor(0xFF00)
            time.sleep(0.1)
            carDetect = 1
        if carDetect == 1 and lastCarDetect == 0:
            print("有车经过.")
            lastCarDetect = 1
        elif carDetect == 0 and lastCarDetect == 1:
            print("车辆已过.")
            lastCarDetect = 0
        pts.appendleft(center)
        for i in range(1, len(pts)):
            if pts[i - 1] is None or pts[i] is None:
                continue
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()


# 用于给双色LED提供颜色转换
def makerobo_set_DoubleColor(col):
    R_val = col >> 8
    G_val = col & 0x00FF
    # 把0-255的范围同比例缩小到0-100之间
    R_val = makerobo_pwm_map(R_val, 0, 255, 0, 100)
    G_val = makerobo_pwm_map(G_val, 0, 255, 0, 100)
    DLED_R.ChangeDutyCycle(R_val)  # 改变占空比
    DLED_G.ChangeDutyCycle(G_val)  # 改变占空比


def makerobo_destroy():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    # GPIO.setmode(GPIO.BOARD)
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)
        GPIO.output(pins[i], GPIO.LOW)
    GPIO.output(Buzzer, GPIO.HIGH)
    GPIO.output(DoubleLED_R, GPIO.LOW)
    GPIO.output(DoubleLED_G, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        makerobo_destroy()
