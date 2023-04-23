#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# －－－－湖南创乐博智能科技有限公司－－－－
#  文件名：09_passive_buzzer.py
#  版本：V2.0
#  author: zhulin
#  说明：无源蜂鸣器实验
#  这是一个无源蜂鸣器模块的程序
#  它可以播放简单的歌曲。
#  你可以尝试自己创作歌曲!
#####################################################
import RPi.GPIO as GPIO
import time

makerobo_Buzzer = 11  # 无源蜂鸣器管脚定义

# 音谱定义
Tone_CL = [0, 131, 147, 165, 175, 196, 211, 248]  # 低C音符的频率
Tone_CM = [0, 262, 294, 330, 350, 393, 441, 495]  # 中C音的频率
Tone_CH = [0, 525, 589, 661, 700, 786, 882, 990]  # 高C音符的频率

# 第一首歌音谱
makerobo_song_1 = [Tone_CM[3], Tone_CM[5], Tone_CM[6], Tone_CM[3], Tone_CM[2], Tone_CM[3], Tone_CM[5], Tone_CM[6],
                   Tone_CH[1], Tone_CM[6], Tone_CM[5], Tone_CM[1], Tone_CM[3], Tone_CM[2], Tone_CM[2], Tone_CM[3],
                   Tone_CM[5], Tone_CM[2], Tone_CM[3], Tone_CM[3], Tone_CL[6], Tone_CL[6], Tone_CL[6], Tone_CM[1],
                   Tone_CM[2], Tone_CM[3], Tone_CM[2], Tone_CL[7], Tone_CL[6], Tone_CM[1], Tone_CL[5]]
# 第1首歌的节拍，1表示1/8拍
makerobo_beat_1 = [1, 1, 3, 1, 1, 3, 1, 1,
                   1, 1, 1, 1, 1, 1, 3, 1,
                   1, 3, 1, 1, 1, 1, 1, 1,
                   1, 2, 1, 1, 1, 1, 1, 1,
                   1, 1, 3]
# 第二首歌音谱
makerobo_song_2 = [Tone_CM[1], Tone_CM[1], Tone_CM[1], Tone_CL[5], Tone_CM[3], Tone_CM[3], Tone_CM[3], Tone_CM[1],
                   Tone_CM[1], Tone_CM[3], Tone_CM[5], Tone_CM[5], Tone_CM[4], Tone_CM[3], Tone_CM[2], Tone_CM[2],
                   Tone_CM[3], Tone_CM[4], Tone_CM[4], Tone_CM[3], Tone_CM[2], Tone_CM[3], Tone_CM[1], Tone_CM[1],
                   Tone_CM[3], Tone_CM[2], Tone_CL[5], Tone_CL[7], Tone_CM[2], Tone_CM[1]]

# 第2首歌的节拍，1表示1/8拍
makerobo_beat_2 = [1, 1, 2, 2, 1, 1, 2, 2,
                   1, 1, 2, 2, 1, 1, 3, 1,
                   1, 2, 2, 1, 1, 2, 2, 1,
                   1, 2, 2, 1, 1, 3]


# GPIO设置函数
def makerobo_setup():
    GPIO.setmode(GPIO.BOARD)  # 采用实际的物理管脚给GPIO口
    GPIO.setwarnings(False)  # 关闭GPIO警告提示
    GPIO.setup(makerobo_Buzzer, GPIO.OUT)  # 设置无源蜂鸣器管脚为输出模式
    global makerobo_Buzz  # 指定一个全局变量来替换gpi.pwm
    makerobo_Buzz = GPIO.PWM(makerobo_Buzzer, 440)  # 设置初始频率为440。
    makerobo_Buzz.start(50)  # 按50%工作定额启动蜂鸣器引脚。


# 循环函数
def makerobo_loop():
    while True:
        #    播放第一首歌音乐...
        for i in range(1, len(makerobo_song_1)):  # 播放第一首歌
            makerobo_Buzz.ChangeFrequency(makerobo_song_1[i])  # 设置歌曲音符的频率
            time.sleep(makerobo_beat_1[i] * 0.5)  # 延迟一个节拍* 0.5秒的音符
        time.sleep(1)  # 等待下一首歌。

        #    播放第二首歌音乐...
        for i in range(1, len(makerobo_song_2)):  # 播放第二首歌
            makerobo_Buzz.ChangeFrequency(makerobo_song_2[i])  # 设置歌曲音符的频率
            time.sleep(makerobo_beat_2[i] * 0.5)  # 延迟一个节拍* 0.5秒的音符


# 释放资源函数
def makerobo_destory():
    makerobo_Buzz.stop()  # 停止蜂鸣器
    GPIO.output(makerobo_Buzzer, 1)  # 设置蜂鸣器管脚为高电平
    GPIO.cleanup()  # 释放资源


# 程序入口
if __name__ == '__main__':
    makerobo_setup()
    try:
        makerobo_loop()
    except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
        makerobo_destory()  # 释放资源
