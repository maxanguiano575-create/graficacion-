import cv2 as cv
import numpy as np
import random
img = np.ones((500, 500, 3), dtype=np.uint8)*255 
x = random.randint(20, 480)   # ← Mínimo 20, máximo 480
y = random.randint(20, 480) 
dx, dy = 5, 3
for i in range(1000):
    img = np.ones((500, 500, 3), dtype=np.uint8)*255 
    
    cv.circle(img, (int (x),int (y)), 20, (0,234,21), -1)
    x += dx
    y += dy 

    if x<20:
        dx =abs(dx)

    elif x>=480:
        dx=-abs(dx)

    if y<20:
        dy=abs(dy)
    elif y>=480:
        dy=-abs(dy)

    cv.imshow('img', img)
    cv.waitKey(1)

cv.waitKey(0)
cv.destroyAllWindows()