import cv2
import os
import pickle
import face_detect
def face_recognize(directory,filename,faces):
    '''
    takes
    '''
    # face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_alt2.xml')  
    imgpath = os.path.join(directory, filename)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("training_data.yml") #NEED training data  
    lables = {}
    with open('lables.pickle', 'rb') as f:
        lables_ = pickle.load(f)       
        lables = {v:k for k,v in lables_.items()}                                        

    image1 = cv2.imread(imgpath)
    # cv2.imshow(image1)
    gray = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('image1',image1)

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]

        id_, conf = recognizer.predict(roi) 
        if conf>60:
            return lables[id_]



    # faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    # if faces is ():
    #     print("No face recognized")
    # else:
    #     print("Face recognized")
    #     moveToPathFile = os.path.join(moveToPath, filename) #destination folder path for the specific image
    #     os.replace(imgpath, moveToPathFile)