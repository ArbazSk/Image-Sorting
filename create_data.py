import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_alt.xml')
capture = cv2.VideoCapture(0)
while(True):
    ret, frame = capture.read()
    count = 0
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)
    while(count <100):
        image_name = str(count) + ".png"
        cv2.imwrite(image_name, frame)
        for (x,y,w,h) in faces:
            cv2.putText(frame,count, (x,y) in faces,cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255), 2)
            cv2.rectangle(frame, (x,y), (x+w,y+h),(250,0,0),2)

        cv2.imshow('Frame', frame)


    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


capture.release()
cv2.destroyAllWindows()