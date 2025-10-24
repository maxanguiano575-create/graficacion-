import numpy as np
import cv2

# Función para generar un solo punto de la elipse en función del parámetro t
def generar_punto_elipse(a, b, t):
    x = int(a * 2* np.cos(t) + 200)  # Desplazamiento para centrar
    y = int(b * np.sin(t) + 200)
    return (x, y)

# Dimensiones de la imagen
img_width, img_height = 800, 800

# Crear una imagen en blanco
imagen = np.zeros((img_height, img_width, 3), dtype=np.uint8)
# Parámetros de la elipse
a = 200  # Semieje mayor
b = 100  # Semieje menor
num_puntos = 1000
# Crear los valores del parámetro t para la animación
t_vals = np.linspace(0, 2 * np.pi, num_puntos)
print(t_vals)
# Bucle de animación
for t in t_vals:
 
    imagen = np.zeros((img_height, img_width, 3), dtype=np.uint8)
    

    punto = generar_punto_elipse(a, b, t)
    

    cv2.circle(imagen, punto, radius=30, color=(0, 255, 0), thickness=-1)

    for t_tray in t_vals:
        pt_tray = generar_punto_elipse(a, b, t_tray)
        cv2.circle(imagen, pt_tray, radius=1, color=(255, 255, 255), thickness=-1)
    

    cv2.imshow('img', imagen)

    cv2.waitKey(10)

cv2.destroyAllWindows()