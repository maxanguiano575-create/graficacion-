import cv2 as cv
import numpy as np

# Tamaño de la ventana
width, height = 500, 500
radius = 20

# Pelota 1
x1, y1 = 100, 100
vx1, vy1 = 5, 3

# Pelota 2
x2, y2 = 300, 200
vx2, vy2 = -4, 6

while True:
    # Fondo blanco
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Dibujar pelotas
    cv.circle(img, (x1, y1), radius, (0, 234, 21), -1)   # verde
    cv.circle(img, (x2, y2), radius, (234, 0, 21), -1)   # rojo
    
    # Mostrar imagen
    cv.imshow("Pin Pon con 2 pelotas", img)
    
    # Mover pelota 1
    x1 += vx1
    y1 += vy1
    if x1 - radius <= 0 or x1 + radius >= width:
        vx1 = -vx1
    if y1 - radius <= 0 or y1 + radius >= height:
        vy1 = -vy1
    
    # Mover pelota 2
    x2 += vx2
    y2 += vy2
    if x2 - radius <= 0 or x2 + radius >= width:
        vx2 = -vx2
    if y2 - radius <= 0 or y2 + radius >= height:
        vy2 = -vy2
    
    # Salir con ESC
    if cv.waitKey(20) & 0xFF == 27:
        break

cv.destroyAllWindows()