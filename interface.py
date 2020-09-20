import cv2
import os
import sys

from os import makedirs
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from win32api import GetSystemMetrics

import face_detect
import object_detect
import face_recognition

screen_res = (GetSystemMetrics(0),GetSystemMetrics(1)) #Get system resolution(Windows OS only)
moveToPath = "h:/testfolder/facefolder"

class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        layout = QVBoxLayout(self)
        # button = QPushButton("something", self)
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

        path = "h:/"

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
        
        #Menu 

        #self.treeview.clicked.connect(self.on_single_clicked)
        self.treeview.doubleClicked.connect(self.integration)

    def move_to_folder(self,directory,filename,make_dir_path):
        current_path = os.path.join(directory, filename)
        dest_path = os.path.join(make_dir_path, filename)
        os.replace(current_path, dest_path)
        print("Moved Successfully {}" .format(dest_path))

    def integration(self,index):
        directory = self.dirModel.fileInfo(index).absoluteFilePath()
        # print(directory)
        # face_detect.detect(path)
        try:
            os.makedirs(moveToPath) #create a new folder as destination
        except OSError:
            print ("Failed to create a new folder %s" % moveToPath)

        #Scanning all images in a given directory
        for filename in os.listdir(directory):
            if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                # print(filename)
                faces = face_detect.detect(directory,filename)
                if faces is ():
                    print("No Faces found in {}".format(filename))
                    object_detected = object_detect.object_det(directory,filename)
                    if object_detected :
                        make_dir_path = os.path.join("h:/testfolder/objectfolder",object_detected)
                         #moving the image to the destination folder
                        if os.path.exists(make_dir_path):
                        	self.move_to_folder(directory,filename,make_dir_path)
                        else:
                        	os.makedirs(make_dir_path)
                        	self.move_to_folder(directory,filename,make_dir_path)
                else:
                    print("Face found! in {}".format(filename))
                    recognized_face = face_recognition.face_recognize(directory, filename, faces)
                    if recognized_face :
                        print("Face Recognized")
                         #moving the image to the destination folder
                        make_dir_path = os.path.join("h:/testfolder/facefolder",recognized_face)
                        if os.path.exists(make_dir_path):
                        	self.move_to_folder(directory,filename,make_dir_path)
                        else:
                        	os.makedirs(make_dir_path)
                        	self.move_to_folder(directory,filename,make_dir_path)
                    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.setWindowTitle("Image Grouper")
    w.setWindowIcon(QtGui.QIcon("icon.png"))
    w.show()
    sys.exit(app.exec_())