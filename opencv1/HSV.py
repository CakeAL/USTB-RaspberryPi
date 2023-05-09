import cv2
import numpy as np

img = cv2.imread("img1.jpg")
# cv2.imshow('BGR', img)
#
# dst = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#
# low_hsv = np.array([0, 43, 46])
# high_hsv = np.array([10, 255, 255])
# dst = cv2.inRange(dst, low_hsv, high_hsv)
# cv2.imshow("result", dst)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cv2.imshow('HSV', img)

dst = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

hsv_low = np.array([0, 0, 0])
hsv_high = np.array([0, 0, 0])


def h_low(value):
    hsv_low[0] = value


def h_high(value):
    hsv_high[0] = value


def s_low(value):
    hsv_low[1] = value


def s_high(value):
    hsv_high[1] = value


def v_low(value):
    hsv_low[2] = value


def v_high(value):
    hsv_high[2] = value


cv2.namedWindow('img')
cv2.createTrackbar('H low', 'img', 0, 180, h_low)
cv2.createTrackbar('H high', 'img', 0, 180, h_high)
cv2.createTrackbar('S low', 'img', 0, 255, s_low)
cv2.createTrackbar('S high', 'img', 0, 255, s_high)
cv2.createTrackbar('V low', 'img', 0, 255, v_low)
cv2.createTrackbar('V high', 'img', 0, 255, v_high)
while True:
    dst = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    dst = cv2.inRange(dst, hsv_low, hsv_high)
    cv2.imshow('dst', dst)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
