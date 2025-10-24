import numpy as np
import cv2 as cv

img = np.ones((500, 500), dtype=np.uint8) * 240

img[30, 30] = 1
img[30, 31] = 1
img[30, 32] = 1
img[30, 33] = 1
img[30, 34] = 1
img[30, 35] = 1

cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()