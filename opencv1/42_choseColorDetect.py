import cv2
import numpy as np
import time

kernel = np.ones((5, 5), np.uint8)
cap = cv2.VideoCapture(0)

time.sleep(0.5)

cap.set(3, 320)
cap.set(4, 240)


def nothing(x):
    pass


cv2.namedWindow('HueComp')
cv2.namedWindow('SatComp')
cv2.namedWindow('ValComp')
cv2.namedWindow('closing')
cv2.namedWindow('tracking')

cv2.createTrackbar('hmin', 'HueComp', 0, 179, nothing)
cv2.createTrackbar('hmax', 'HueComp', 10, 179, nothing)
cv2.createTrackbar('smin', 'SatComp', 96, 255, nothing)
cv2.createTrackbar('smax', 'SatComp', 255, 255, nothing)
cv2.createTrackbar('vmin', 'ValComp', 186, 255, nothing)
cv2.createTrackbar('vmax', 'ValComp', 255, 255, nothing)

while True:
    buzz = 0
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hue, sat, val = cv2.split(hsv)
    hmn = cv2.getTrackbarPos('hmin', 'HueComp')
    hmx = cv2.getTrackbarPos('hmax', 'HueComp')
    smn = cv2.getTrackbarPos('smin', 'SatComp')
    smx = cv2.getTrackbarPos('smax', 'SatComp')
    vmn = cv2.getTrackbarPos('vmin', 'ValComp')
    vmx = cv2.getTrackbarPos('vmax', 'ValComp')
    # 应用阈值
    hthresh = cv2.inRange(np.array(hue), np.array(hmn), np.array(hmx))
    sthresh = cv2.inRange(np.array(sat), np.array(smn), np.array(smx))
    vthresh = cv2.inRange(np.array(val), np.array(vmn), np.array(vmx))
    # h s 和 v
    tracking = cv2.bitwise_and(hthresh, cv2.bitwise_and(sthresh, vthresh))
    # 一些morpholigical过滤
    dilation = cv2.dilate(tracking, kernel, iterations = 1)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    closing = cv2.GaussianBlur(closing, (5, 5), 0)

    circles = cv2.HoughCircles(closing, cv2.HOUGH_GRADIENT, 2, 120, param1=120, param2=50, minRadius=10, maxRadius=0)

    if circles is not None:
        x, y, r = circles[0][0]
        x_p = int(round(x))
        print(x_p)
        for i in circles[0,:]:
            if int(round(i[2])) < 30:  # 用绿色画
                cv2.circle(frame, (int(round(i[0])), int(round(i[1]))), int(round(i[2])), (0, 255, 0), 5)
                cv2.circle(frame, (int(round(i[0])), int(round(i[1]))), 2, (0,255,0), 10)
            elif int(round(i[2])) > 35:  # 用红色画
                cv2.circle(frame, (int(round(i[0])), int(round(i[1]))), int(round(i[2])), (0, 0, 255), 5)
                cv2.circle(frame, (int(round(i[0])), int(round(i[1]))), 2, (0, 0, 255), 10)
    cv2.imshow('HueComp', hthresh)
    cv2.imshow('SatComp', sthresh)
    cv2.imshow('ValComp', vthresh)
    cv2.imshow('closing', closing)
    cv2.imshow('tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

