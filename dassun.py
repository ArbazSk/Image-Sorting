import cv2
import os
import sys
import threading
import numpy as np
import pickle

from collections import Counter
from os import makedirs
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from win32api import GetSystemMetrics

screen_res = (GetSystemMetrics(0),GetSystemMetrics(1)) #Get system resolution(Windows OS only)
moveToPath = "f:/testfolder/facefolder"

def face_detect(directory):
    #directory = "d:/testfolder" #current folder
    #imageList = []
    #destination folder path
    try:
        os.makedirs(moveToPath) #create a new folder as destination
    except OSError:
        print ("Failed to create a new folder %s" % moveToPath)

    #Scanning all images in a given directory
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"): 
            #imageList.append(filename)

            face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_alt2.xml')
            imgpath = os.path.join(directory, filename) #path for the specific image 
            img = cv2.imread(imgpath) #reading the image from current folder
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.0485258, 6) # returns dimensions for rectangle around detected face

            #Checking if faces are detected or not
            if faces is ():
                print("No Faces found in {}".format(filename))
                object_detect(directory,filename)
            else:
                print("Face found! in {}".format(filename))
                face_recog(directory,filename)
                #moving the image to the destination folder

class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        layout = QVBoxLayout(self)
        button = QPushButton("something", self)
        self.top = 128
        self.left = 128
        self.width = screen_res[0]/1.5
        self.height = screen_res[1]/1.5
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.treeview = QTreeView()
        #self.listview = QListView()
        layout.addWidget(button)
        layout.addWidget(self.treeview)
        #layout.addWidget(self.listview)

        path = "f:/"

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

        #self.treeview.clicked.connect(self.on_single_clicked)
        self.treeview.doubleClicked.connect(self.on_clicked)

    #def on_single_clicked(self, index):
        #print("Hallelujah!")
    def on_clicked(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        face_detect(path)
        
        #self.listview.setRootIndex(self.fileModel.setRootPath(path))

def move_to_folder(directory,filename,make_dir_path):
	current_path = os.path.join(directory, filename)
	dest_path = os.path.join(make_dir_path, filename)
	os.replace(current_path, dest_path)

def object_detect(directory, filename):
#for filename in os.listdir(directory):
#	if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
	tagList = []
	args = {'image': '', 'yolo': 'yolo-coco', 'confidence': 0.5, 'threshold': 0.3}
	args['image'] = os.path.join(directory,filename)

	labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
	LABELS = open(labelsPath).read().strip().split("\n")

	np.random.seed(42)

	weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
	configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

	net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

	image = cv2.imread(args["image"])
	(H, W) = image.shape[:2]

	ln = net.getLayerNames()
	ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	net.setInput(blob)
	
	layerOutputs = net.forward(ln)

	boxes = []
	confidences = []
	classIDs = []

	for output in layerOutputs:
		for detection in output:

			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			if confidence > args["confidence"]:
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
			args["threshold"])

	if len(idxs) == 0:
		pass
	else:
		for i in idxs.flatten():
				#if confidences[i] >= 0.9:
			tagList.append(LABELS[classIDs[i]])
			count = Counter(tagList)
		a, b = count.keys(), count.values()
		keysList = list(a)
		#valuesList = list(b)
		print(keysList[0])

		make_dir_path = os.path.join("f:/",keysList[0])
		if os.path.exists(make_dir_path):
			move_to_folder(directory,filename,make_dir_path)
		else:
            #obj_dest = os.path.join(keysList[0], filename)
			os.makedirs(make_dir_path)
			move_to_folder(directory,filename,make_dir_path)

def face_recog(directory,filename):
    face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_alt2.xml')
    imgpath = os.path.join(directory, filename)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("training_data.yml") #NEED training data  
    lables = {}
    with open('lables.pickle', 'rb') as f:
        lables_ = pickle.load(f)       
        lables = {v:k for k,v in lables_.items()}                                                                 

    image1 = cv2.imread('test/53.jpg')
    gray = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('image1',image1)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    if faces is ():
        print("No face recognized")
    else:
        print("Face recognized")
        moveToPathFile = os.path.join(moveToPath, filename) #destination folder path for the specific image
        os.replace(imgpath, moveToPathFile)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.setWindowTitle("Image Grouper")
    w.setWindowIcon(QtGui.QIcon("icon.png"))
    w.show()
    #thread1 = threading.Thread(target=Widget, args=(QWidget))
    #thread2 = threading.Thread(target=face_detect)
    #thread1.start()
    #thread2.start()
    sys.exit(app.exec_())