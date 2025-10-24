import cv2
import numpy as np
import threading
import time


lock = threading.Lock()

pizarron = np.zeros((500, 500, 3), dtype=np.uint8)

img_oculta = cv2.imread("oculta.png")
if img_oculta is None:
   
    img_oculta = np.zeros((60, 60, 3), dtype=np.uint8)
    cv2.rectangle(img_oculta, (15, 15), (45, 45), (0, 255, 0), -1)
    cv2.putText(img_oculta, "OK", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

img_oculta = cv2.resize(img_oculta, (60, 60))
h, w, _ = img_oculta.shape

posiciones = [(50, 60), (300, 100), (400, 200), (120, 350), (250, 420)]

pizarron_real = pizarron.copy()
for (x, y) in posiciones:
    pizarron_real[y:y+h, x:x+w] = img_oculta

pizarron_visible = pizarron.copy()

cv2.namedWindow("Buscando Imágenes Ocultas", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Buscando Imágenes Ocultas", 700, 700)


posiciones_encontradas = []

def buscar(x_inicio, x_fin, nombre_hilo):
    global pizarron_visible, posiciones_encontradas
    
    for y in range(0, pizarron.shape[0] - h + 1):
        for x in range(x_inicio, min(x_fin, pizarron.shape[1] - w + 1)):
            bloque = pizarron_real[y:y+h, x:x+w]
            if np.array_equal(bloque, img_oculta):
                print(f"[{nombre_hilo}] ¡Imagen encontrada en ({x}, {y})!")
                
               
                with lock:
                    if (x, y) not in posiciones_encontradas:
                        posiciones_encontradas.append((x, y))
                        
                   
                        pizarron_temp = pizarron_visible.copy()
                        cv2.rectangle(pizarron_temp, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        cv2.imshow("Buscando Imágenes Ocultas", pizarron_temp)
                        cv2.waitKey(1)
                        time.sleep(0.5)

                        pizarron_visible[y:y+h, x:x+w] = img_oculta
                        cv2.imshow("Buscando Imágenes Ocultas", pizarron_visible)
                        cv2.waitKey(1)
                        time.sleep(0.5)
                
             
                break


cv2.imshow("Buscando Imágenes Ocultas", pizarron_visible)
cv2.waitKey(500)

print("Buscando imágenes ocultas...")


ancho = pizarron.shape[1]
franja = ancho // 5
hilos = []

for i in range(5):
    x_inicio = i * franja
    x_fin = (i + 1) * franja if i < 4 else ancho
    hilo = threading.Thread(target=buscar, args=(x_inicio, x_fin, f"Hilo {i+1}"))
    hilos.append(hilo)


for hilo in hilos:
    hilo.start()

#
for hilo in hilos:
    hilo.join()

print("¡Se encontraron todas las imágenes!")
cv2.waitKey(0)
cv2.destroyAllWindows()