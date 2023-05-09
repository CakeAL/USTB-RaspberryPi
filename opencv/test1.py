import numpy as np
import cv2

img1 = cv2.imread("img1.jpg", cv2.IMREAD_COLOR)
print(img1.shape)
cv2.imshow('image1', img1)
# cv2.waitKey(0)

img2 = cv2.imread("img1.jpg", cv2.IMREAD_GRAYSCALE)
print(img2.shape)
cv2.imshow('image2', img2)
# cv2.waitKey(0)


img3 = cv2.imread("img1.jpg", cv2.IMREAD_UNCHANGED)
print(img3.shape)
cv2.imshow('image3', img3)
# cv2.waitKey(0)

imgfilp = cv2.flip(img2, 0)
cv2.imshow('image4', imgfilp)
cv2.waitKey(0)
cv2.imwrite("new.jpg", imgfilp)
cv2.destroyAllWindows()

