import cv2 as cv
import numpy as np

img = np.ones((500, 500, 3), dtype=np.uint8)*255 

for i in range(400):
    img = np.ones((500, 500, 3), dtype=np.uint8)*255 
    cv.circle(img, (0+i, 0+i), 20, (0,234,21), -1)# SOLO AQUI SE CAMBIA PARA EL PING
    cv.imshow('img', img)
    cv.waitKey(40)

cv.waitKey(0)
cv.destroyAllWindows()