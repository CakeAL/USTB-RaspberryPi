from collections import deque
import numpy as np
import argparse
import imutils
import cv2

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
