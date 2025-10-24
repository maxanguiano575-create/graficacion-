import cv2 as cv
import numpy as np
import math


img = cv.imread('pa.png', 0)
x, y = img.shape
print(f"Tamaño original: {x}x{y}")


scale_factor = 2
new_x, new_y = int(x * scale_factor), int(y * scale_factor)
scaled_img = np.zeros((new_x, new_y), dtype=np.uint8)

print("Escalando imagen 2x con vecino más cercano...")
print(f"Tamaño escalado: {new_x}x{new_y}")
for i in range(new_x):
    for j in range(new_y):
     
        orig_i = min(int(i / scale_factor), x-1)
        orig_j = min(int(j / scale_factor), y-1)
        scaled_img[i, j] = img[orig_i, orig_j]


angle = 45
theta = math.radians(angle)


cos_ang = abs(math.cos(theta))
sin_ang = abs(math.sin(theta))
rot_x = int(new_x * cos_ang + new_y * sin_ang)
rot_y = int(new_x * sin_ang + new_y * cos_ang)

rotated_img = np.zeros((rot_x, rot_y), dtype=np.uint8)
print(f"Tamaño rotado: {rot_x}x{rot_y}")

# Centros
cx, cy = new_x // 2, new_y // 2
rot_cx, rot_cy = rot_x // 2, rot_y // 2

print("Rotando 45° con filtro bilineal...")
for i in range(rot_x):
    for j in range(rot_y):
      
        rel_x = j - rot_cy
        rel_y = i - rot_cx
        
   
        orig_x = rel_x * math.cos(theta) + rel_y * math.sin(theta) + cy
        orig_y = -rel_x * math.sin(theta) + rel_y * math.cos(theta) + cx
        
      
        if 0 <= orig_x < new_y-1 and 0 <= orig_y < new_x-1:
            x0 = int(orig_x)
            y0 = int(orig_y)
            x1 = min(x0 + 1, new_y - 1)
            y1 = min(y0 + 1, new_x - 1)
            
           
            wx = orig_x - x0
            wy = orig_y - y0
            
            
            p00 = scaled_img[y0, x0]
            p01 = scaled_img[y0, x1]
            p10 = scaled_img[y1, x0]
            p11 = scaled_img[y1, x1]
            
            value = (1 - wx) * (1 - wy) * p00 + \
                    wx * (1 - wy) * p01 + \
                    (1 - wx) * wy * p10 + \
                    wx * wy * p11
            
            rotated_img[i, j] = np.clip(value, 0, 255)


cv.imshow('1. Imagen Original', img)
cv.imshow('2. Imagen Escalada 2x (Vecino Cercano)', scaled_img)
cv.imshow('3. Imagen Rotada 45° (Bilineal)', rotated_img)

print("Presiona cualquier tecla para cerrar las ventanas...")
cv.waitKey(0)
cv.destroyAllWindows()