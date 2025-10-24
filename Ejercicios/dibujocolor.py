import cv2
import numpy as np


camara = cv2.VideoCapture(0)

# Creamos un lienzo vacío
ret, cuadro = camara.read()
lienzo = np.zeros_like(cuadro)

# Rango del color rojo en HSV
u_bajo = np.array([0, 150, 50])
u_alto = np.array([10, 255, 255])

punto_anterior = None
umbral_distancia = 50  # para evitar trazos largos falsos

while True:
    ret, cuadro = camara.read()
    if not ret:
        break
    
    hsv = cv2.cvtColor(cuadro, cv2.COLOR_BGR2HSV)
    mascara = cv2.inRange(hsv, u_bajo, u_alto)

    # Momentos de la máscara (para calcular el centroide)
    momentos = cv2.moments(mascara)
    if momentos["m00"] > 0:  # hay píxeles del color buscado
        cx = int(momentos["m10"] / momentos["m00"])
        cy = int(momentos["m01"] / momentos["m00"])
        punto_actual = (cx, cy)

        # Dibujar punto en la cámara
        cv2.circle(cuadro, punto_actual, 5, (0, 0, 255), -1)

        # Dibujar línea en el lienzo si el salto no es muy grande
        if punto_anterior is not None:
            distancia = np.linalg.norm(np.array(punto_actual) - np.array(punto_anterior))
            if distancia < umbral_distancia:
                cv2.line(lienzo, punto_anterior, punto_actual, (0, 255, 0), 5)

        punto_anterior = punto_actual
    else:
        punto_anterior = None

    combinado = cv2.add(cuadro, lienzo)

    cv2.imshow("Dibujo en vivo", combinado)
    cv2.imshow("Mascara de color", mascara)
    cv2.imshow("Lienzo", lienzo)
    tecla = cv2.waitKey(1) & 0xFF
    if tecla == 27:  # ESC para salir
        break
    elif tecla == ord('c'):  # limpiar lienzo
        lienzo = np.zeros_like(cuadro)

camara.release()
cv2.destroyAllWindows()