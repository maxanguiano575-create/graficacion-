import cv2 as cv 
import numpy as np

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)

frame_count = 0
pupil_direction = 1  
tongue_direction = 1  
pupil_offset = 0
tongue_length = 0

while True:
    ret, img = cap.read()
    if not ret:
        break
        
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)
    
    for(x, y, w, h) in rostros:
        img = cv.rectangle(img, (x, y), (x+w, y+h), (234, 23, 23), 5)
        img = cv.rectangle(img, (x, int(y+h/2)), (x+w, y+h), (0, 255, 0), 5)
        
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)), 21, (0, 0, 0), 2)
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)), 21, (0, 0, 0), 2)
        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)), 20, (255, 255, 255), -1)
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)), 20, (255, 255, 255), -1)
        
        max_pupil_offset = 8
        pupil_offset += pupil_direction * 0.5
        
        if pupil_offset >= max_pupil_offset:
            pupil_direction = -1
        elif pupil_offset <= -max_pupil_offset:
            pupil_direction = 1
            
        img = cv.circle(img, (x + int(w*0.3) + int(pupil_offset), y + int(h*0.4)), 5, (0, 0, 255), -1)
        img = cv.circle(img, (x + int(w*0.7) + int(pupil_offset), y + int(h*0.4)), 5, (0, 0, 255), -1)
        
        nose_width = int(w * 0.15)
        nose_height = int(h * 0.1)
        nose_top = (x + w//2, y + int(h*0.5))
        nose_left = (x + w//2 - nose_width//2, y + int(h*0.5) + nose_height)
        nose_right = (x + w//2 + nose_width//2, y + int(h*0.5) + nose_height)
        
        triangle_cnt = np.array([nose_top, nose_left, nose_right])
        img = cv.drawContours(img, [triangle_cnt], 0, (0, 100, 200), -1)
        img = cv.drawContours(img, [triangle_cnt], 0, (0, 0, 0), 2)
        
        ear_width = int(w * 0.15)
        ear_height = int(h * 0.25)
        
        left_ear_center = (x - ear_width//2, y + int(h*0.4))
        img = cv.ellipse(img, left_ear_center, (ear_width//2, ear_height//2), 0, 0, 360, (200, 150, 100), -1)
        img = cv.ellipse(img, left_ear_center, (ear_width//2, ear_height//2), 0, 0, 360, (0, 0, 0), 2)
        
        right_ear_center = (x + w + ear_width//2, y + int(h*0.4))
        img = cv.ellipse(img, right_ear_center, (ear_width//2, ear_height//2), 0, 0, 360, (200, 150, 100), -1)
        img = cv.ellipse(img, right_ear_center, (ear_width//2, ear_height//2), 0, 0, 360, (0, 0, 0), 2)
        
        mouth_width = int(w * 0.4)
        mouth_height = int(h * 0.1)
        mouth_center = (x + w//2, y + int(h*0.7))
        
        img = cv.ellipse(img, mouth_center, (mouth_width//2, mouth_height//2), 0, 0, 180, (0, 0, 255), -1)
        img = cv.ellipse(img, mouth_center, (mouth_width//2, mouth_height//2), 0, 0, 180, (0, 0, 0), 2)
        
        max_tongue_length = int(h * 0.15)
        tongue_length += tongue_direction * 2
        
        if tongue_length >= max_tongue_length:
            tongue_direction = -1
        elif tongue_length <= 0:
            tongue_direction = 1
            
        if tongue_length > 0:
            tongue_radius = int(w * 0.06)
            tongue_center = (x + w//2, y + int(h*0.7) + tongue_length)
            
            img = cv.circle(img, tongue_center, tongue_radius, (255, 0, 0), -1)
            img = cv.circle(img, tongue_center, tongue_radius, (0, 0, 0), 2)
        
        cv.putText(img, "Presiona 'q' para salir", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    frame_count += 1
    
    cv.imshow('img', img)
    if cv.waitKey(1) == ord('q'):
        break
    
cap.release()
cv.destroyAllWindows()
