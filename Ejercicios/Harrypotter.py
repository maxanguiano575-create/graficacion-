import cv2
import numpy as np

# Captura de video desde la cámara (0 = cámara predeterminada)
cap = cv2.VideoCapture(0)

# Espera 2 segundos para que la cámara se estabilice
cv2.waitKey(2000)

# Capturar el fondo en ese momento
ret, background = cap.read()
if not ret:  # Si no se pudo capturar el fondo
    print("Error al capturar el fondo.")
    cap.release()  # Liberar la cámara
    exit()         # Salir del programa

# Bucle principal mientras la cámara esté abierta
while cap.isOpened():
    ret, frame = cap.read()  # Captura un nuevo cuadro
    if not ret:  # Si no se pudo capturar el cuadro
        break

    # Convertir el cuadro de BGR a HSV (más fácil para detección de color)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir el rango de color verde en HSV (ajustable según la tela que uses)
    lower_green = np.array([80, 40, 40])
    upper_green = np.array([145, 255, 255])

    # Crear una máscara que detecta solo el color verde
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Invertir la máscara para obtener las áreas que NO son verdes
    mask_inv = cv2.bitwise_not(mask)

    # Aplicar la máscara invertida a la imagen original
    # Esto deja visibles las partes que no son verdes
    res1 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Aplicar la máscara original al fondo
    # Esto cubre las partes verdes con el fondo capturado
    res2 = cv2.bitwise_and(background, background, mask=mask)

    # Combinar las dos imágenes: partes no verdes del cuadro + fondo en lugar del verde
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) 

    # Mostrar el resultado final (efecto de invisibilidad)
    cv2.imshow("Capa de Invisibilidad", final_output)

    # Mostrar la máscara para ver qué se está detectando como verde
    cv2.imshow('mask', mask)

    # Presionar 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()