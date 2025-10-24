import cv2 as cv
import numpy as np
import math


img = cv.imread('tr.png', 0)

x, y = img.shape

rotated_img = np.zeros((x*2, y*2), dtype=np.uint8)
xx, yy = rotated_img.shape

cx, cy = int(x  // 2), int(y  // 2)

angle = 45
theta = math.radians(angle)


for i in range(x):
    for j in range(y):
        new_x = int((j - cx) * math.cos(theta) - (i - cy) * math.sin(theta) + cx) 
        new_y = int((j - cx) * math.sin(theta) + (i - cy) * math.cos(theta) + cy)
        if 0 <= new_x < y and 0 <= new_y < x:
            rotated_img[new_y, new_x] = img[i, j]

cv.imshow('Imagen Original', img)
cv.imshow('Imagen Rotada (modo raw)', rotated_img)
cv.waitKey(0)
cv.destroyAllWindows()