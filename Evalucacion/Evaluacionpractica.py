import cv2 as cv

rostro = cv.CascadeClassifier(r'C:\Users\Max\Documents\Graficacion\Evalucacion\haarcascade_frontalface_alt.xml')


if rostro.empty():
    print(" No se pudo cargar")
    exit()
else:
    print(" cargo correctamente")

cap = cv.VideoCapture(0)


dx, dy = 2, 2
pupil_offset_x, pupil_offset_y = 0, 0

while True:
    ret, img = cap.read()
    if not ret:
        print(" Error ")
        break

    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)

    
    pupil_offset_x += dx
    pupil_offset_y += dy
    if abs(pupil_offset_x) > 5:
        dx = -dx
    if abs(pupil_offset_y) > 5:
        dy = -dy

    for (x, y, w, h) in rostros:
     
        escala = max(0.3, min(1.0, w / 400))

        radio_ojo = int(25 * escala)
        radio_pupila = int(10 * escala)

        ojo_izq = (x + int(w * 0.3), y + int(h * 0.4))
        ojo_der = (x + int(w * 0.7), y + int(h * 0.4))

     
        cv.circle(img, ojo_izq, radio_ojo, (255, 255, 255), -1)
        cv.circle(img, ojo_der, radio_ojo, (255, 255, 255), -1)
        cv.circle(img, ojo_izq, radio_ojo, (0, 0, 0), 2)
        cv.circle(img, ojo_der, radio_ojo, (0, 0, 0), 2)

 
        pupila_izq = (ojo_izq[0] + pupil_offset_x, ojo_izq[1] + pupil_offset_y)
        pupila_der = (ojo_der[0] + pupil_offset_x, ojo_der[1] + pupil_offset_y)

        cv.circle(img, pupila_izq, radio_pupila, (0, 0, 255), -1)
        cv.circle(img, pupila_der, radio_pupila, (0, 0, 255), -1)

    cv.imshow(' ojos dinámicos', img)

    if cv.waitKey(10) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
