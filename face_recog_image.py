import cv2
import numpy as  np
import pickle

face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_alt.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("training_data.yml")    
lables = {}
with open('lables.pickle', 'rb') as f:
    lables_ = pickle.load(f)       
    lables = {v:k for k,v in lables_.items()}                                                                 

image1 = cv2.imread('test/53.jpg')
gray = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
# cv2.imshow('image1',image1)

faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

for (x, y, w, h) in faces:
    roi = gray[y:y+h, x:x+w]

    id_, conf = recognizer.predict(roi) 
    if conf>90:
        # print(id_)
        print(lables[id_])
        cv2.putText(gray, lables[id_], (x,y), cv2.FONT_HERSHEY_PLAIN, 1, (250,255,255), 2)
    # img_ = "image_from_face.png"
    # cv2.imwrite(img_, roi)

    cv2.rectangle(gray, (x,y), (x+w,y+h),(250,0,0),2)
    cv2.imshow('Face',gray)

cv2.waitKey()
cv2.destroyAllWindows()
