import cv2 as cv
import numpy as np
import random
import math

img = np.ones((500, 500, 3), dtype=np.uint8)*255 
x = random.randint(40, 460)  
y = random.randint(40, 460) 
z = random.randint(40, 460)   
w = random.randint(40, 460) 
dx, dy, dz, dw = 3, 3, 4, 2 

for i in range(1000):
    img = np.ones((500, 500, 3), dtype=np.uint8)*255 
    
    cv.circle(img, (int(z), int(w)), 20, (0, 234, 21), -1)
    cv.circle(img, (int(x), int(y)), 20, (234, 0, 21), -1)
    
    x += dx
    y += dy 
    z += dz
    w += dw 
    
    
    distance = math.sqrt((x - z)**2 + (y - w)**2)
    if distance < 40:  
       
        dx, dz = dz, dx
        dy, dw = dw, dy 

    if x <= 20 or x >= 480:
        dx = -dx
    if y <= 20 or y >= 480:
        dy = -dy
 
    if z <= 20 or z >= 480:
        dz = -dz
    if w <= 20 or w >= 480:
        dw = -dw

    cv.imshow('Dos círculos rebotando', img)
    

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()