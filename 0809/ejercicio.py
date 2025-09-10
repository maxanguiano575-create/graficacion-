import cv2 as cv #importa la libreria de open cvcv
import numpy as np #importa numpy 

cap = cv.VideoCapture(0)# abre camara
while(True):# bucle para para captar video 
    ret, img = cap.read() # captura un frame de la camara
    if ret: # si la camara funciona correctamente
        cv.imshow('video', img)# muestra el video 
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV) # convierte bgr a hsv 
        uba=(90, 255, 255) # limite del rago de color 
        ubb=(40, 40 ,40)# limite inferior del rango de color 
        mask = cv.inRange(hsv, ubb, uba)# crea una mascara 
        res = cv.bitwise_and(img, img, mask=mask)# aplica la mascara a la imagen original 
        cv.imshow('res', res)# muestra mascara con el filtrado 
        cv.imshow('mask', mask)# muestra mascara blanco y negro 
        k =cv.waitKey(1) & 0xFF# espera la letra esc para cerrar el programa 
        if k == 27 :
            break
    else:
        break# si no hay frame rompe el bucle 
cap.release()# libera camara y cierra todo
cv.destroyAllWindows()