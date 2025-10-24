import numpy as np
import cv2

width, height = 1000, 1000  
img = np.ones((height, width, 3), dtype=np.uint8)*255


a, b = 150, 100  
k = 0.7
theta_increment = 0.05  
max_theta = 2 * np.pi  

# Centro de la imagen
center_x, center_y = width // 2, height // 2

theta = 0  # Ángulo inicial

while True:  # Bucle infinito
    # Limpiar la imagen
    img = np.ones((width, height, 3), dtype=np.uint8) * 255
    
    # Dibujar la curva completa desde 0 hasta theta
    for t in np.arange(0, theta, theta_increment):
        # Calcular las coordenadas paramétricas (x, y) para la curva de Limacon
        r = a + b * np.cos(k * t)
        x = int(center_x + r * np.cos(t))
        y = int(center_y + r * np.sin(t))
        
 
        cv2.circle(img, (x-2, y-2), 3, (0, 0, 0), -1)  # Color rojo
    

    cv2.imshow("Parametric Animation", img)
    img = np.ones((width, height, 3), dtype=np.uint8) * 255
    
    # Incrementar el ángulo
    theta += theta_increment
    

    if cv2.waitKey(30) & 0xFF == 27:  # Esperar 30ms, salir con 'ESC'
        break


cv2.destroyAllWindows()