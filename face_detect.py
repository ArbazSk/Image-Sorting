import cv2
import os

def detect(directory,filename):
    '''
    Detect Faces in a directory and return a list containing the location of the faces.
    Input:- takes directory where images are present.
    Output:- return list which containt location of faces
    '''
    # face_data = {}
    face_cascade = cv2.CascadeClassifier('pre-trained_data/haarcascades/haarcascade_frontalface_alt.xml')
    # face_cascade = cv2.CascadeClassifier('G:\Engeering Project Clg\Image-Sorting\data\haarcascades\haarcascade_frontalface_alt.xml')
    imgpath = os.path.join(directory, filename) #path for the specific image 
    img = cv2.imread(imgpath) #reading the image from current folder
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray, 1.0485258, 6) # returns dimensions for rectangle around detected face
    #Checking if faces are detected or not
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    # face_data[filename] = faces
    # if faces is ():
    #     print("No Faces found in {}".format(filename))
    #     return
    # else:
    #     print("Face is detected in {}".format(imgpath))
    #     return faces
    return faces
                

