import cv2 as cv
import numpy as np

# Cargar la imagen en escala de grises
img = cv.imread('Gato.png', 0)

x, y = img.shape

scale_x, scale_y = 2, 2

scaled_img = np.zeros((int(x * scale_y), int(y * scale_x)), dtype=np.uint8)


for i in range(x):
    for j in range(y):
        scaled_img[i*2, j*2] = img[i, j]


for i in range(scaled_img.shape[0]):
    for j in range(scaled_img.shape[1]):
        if scaled_img[i, j] == 0: 
            # se busca el vecino más cercano que no este apagado
            found = False
            radius = 1
            while not found and radius < max(scaled_img.shape):
                
                for di in range(-radius, radius + 1):
                    for dj in range(-radius, radius + 1):
                        ni, nj = i + di, j + dj
                        if (0 <= ni < scaled_img.shape[0] and 
                            0 <= nj < scaled_img.shape[1] and 
                            scaled_img[ni, nj] != 0):
                            scaled_img[i, j] = scaled_img[ni, nj]
                            found = True
                            break
                    if found:
                        break
                if found:
                    break
                radius += 1

scaled_img_correct = np.zeros((int(x * scale_y), int(y * scale_x)), dtype=np.uint8)
for i in range(scaled_img_correct.shape[0]):
    for j in range(scaled_img_correct.shape[1]):
    
        orig_i = min(int(i / scale_y), x - 1)
        orig_j = min(int(j / scale_x), y - 1)
        scaled_img_correct[i, j] = img[orig_i, orig_j]


cv.imshow('Imagen Original', img)
cv.imshow('Tu Imagen con Huecos', scaled_img)  
cv.imshow('Imagen Rellenada', scaled_img)    
cv.imshow('Imagen Escalada Correcta', scaled_img_correct)  
cv.waitKey(0)
cv.destroyAllWindows()