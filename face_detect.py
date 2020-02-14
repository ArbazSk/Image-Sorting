import cv2
import os
import sys
import threading
import numpy as np
import pickle

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from win32api import GetSystemMetrics

screen_res = (GetSystemMetrics(0),GetSystemMetrics(1)) #Get system resolution(Windows OS only)
moveToPath = "F:/testfolder/facefolder"

def face_detect(directory):
    #directory = "d:/testfolder" #current folder
    #imageList = []
    #destination folder path
    try:
        os.mkdir(moveToPath) #create a new folder as destination
    except OSError:
        print ("Failed to create a new folder %s" % moveToPath)

    #Scanning all images in a given directory
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"): 
            #imageList.append(filename)

            face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_alt.xml')
            imgpath = os.path.join(directory, filename) #path for the specific image 
            img = cv2.imread(imgpath) #reading the image from current folder
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.0485258, 6) # returns dimensions for rectangle around detected face

            #Checking if faces are detected or not
            if faces is ():
                print("No Faces found in {}".format(filename))
            else:
                print("Face found! in {}".format(filename))
                face_recognition(directory)
                #moveToPathFile = os.path.join(moveToPath, filename) #destination folder path for the specific image
                #os.replace(imgpath, moveToPathFile) #moving the image to the destination folder

def face_recognition(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_alt.xml')
            imgpath = os.path.join(directory, filename)
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read("training_data.yml")    
            lables = {}
            with open('lables.pickle', 'rb') as f:
                lables_ = pickle.load(f)       
                lables = {v:k for k,v in lables_.items()}                                                                 

            image1 = cv2.imread('test/53.jpg')
            gray = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('image1',image1)

            facesRecog = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            if facesRecog is ():
                print("No Faces recognized in {}".format(filename))
            else:
                print("Face recognized in {}".format(filename))
                moveToPathFile = os.path.join(moveToPath, filename) #destination folder path for the specific image
                os.replace(imgpath, moveToPathFile) #moving the image to the destination folder


    '''for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]

        id_, conf = recognizer.predict(roi) 
        if conf>50:
            # print(id_)
            # print(lables[id_])
            cv2.putText(gray, lables[id_], (x,y), cv2.FONT_HERSHEY_PLAIN, 1, (250,255,255), 2)
        #img_ = "image_from_face.png"
        #cv2.imwrite(img_, roi)

        #cv2.rectangle(gray, (x,y), (x+w,y+h),(250,0,0),2)
        #cv2.imshow('Face',gray)

    #cv2.waitKey()
    #cv2.destroyAllWindows()'''
    


class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        layout = QVBoxLayout(self)
        # button = QPushButton("Fat && useless button", self)
        self.top = 128
        self.left = 128
        self.width = screen_res[0]/1.5
        self.height = screen_res[1]/1.5
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.treeview = QTreeView()
        #self.listview = QListView()
        # layout.addWidget(button)
        layout.addWidget(self.treeview)
        #layout.addWidget(self.listview)

        path = "F:/"

        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(QDir().dirName())
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        #self.fileModel = QFileSystemModel()
        #self.fileModel.setFilter(QDir.NoDotAndDotDot |  QDir.Files)

        self.treeview.setModel(self.dirModel)
        #self.listview.setModel(self.fileModel)

        self.treeview.setRootIndex(self.dirModel.index(path))
        #self.listview.setRootIndex(self.fileModel.index(path))

        self.header = self.treeview.header()
        #header.setStretchLastSection(False)
        self.header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.header.setSectionHidden(1, True)
        self.header.setSectionHidden(2, True)
        self.header.setSectionHidden(3, True)
        #header.resizeSection(1, 100)

        self.treeview.clicked.connect(self.on_single_clicked)
        self.treeview.doubleClicked.connect(self.on_clicked)

    def on_single_clicked(self, index):
        # print("Hallelujah!")
        pass

    def on_clicked(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        face_detect(path)
        
        #self.listview.setRootIndex(self.fileModel.setRootPath(path))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.setWindowTitle("Face Detector (name subject to change)")
    w.setWindowIcon(QtGui.QIcon("icon.png"))
    w.show()
    thread1 = threading.Thread(target=Widget, args=(QWidget))
    thread2 = threading.Thread(target=face_detect)
    # thread1.start()
    # thread2.start()
    sys.exit(app.exec_())