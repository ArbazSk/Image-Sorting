import os
from PIL import Image
import numpy as np
import cv2
import pickle

face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_alt.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR,'image')

y_lable = []
x_train = []
lable_id = {}
current_id = 0

for root, dirs, files in os.walk(image_dir):
    for filename in files:
            if filename.endswith("png") or filename.endswith("jpg") or filename.endswith('jpeg'):
                path = os.path.join(root, filename)
                # print(path)
                # lable = os.path.basename(os.path.dirname(path)).replace(" ", "-")
                lable = os.path.basename(root).replace(" ", "-")
                # print(lable)
                if not lable in lable_id:
                    lable_id[lable] = current_id
                    current_id += 1
                id_ = lable_id[lable]
                # print(lable_id)

                pil_image = Image.open(path).convert("L") # Converting to grayscale
                finale_img = pil_image.resize((500,500),Image.ANTIALIAS)
                image_array = np.array(finale_img)
                # print(image_array)
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.2, minNeighbors=5)

                for (x, y, w, h) in faces:
                    roi = image_array[y:y+h, x:x+w]
                    x_train.append(roi)
                    y_lable.append(id_)

print(lable_id)
with open('lables.pickle', 'wb') as f:
    pickle.dump(lable_id, f)


recognizer.train(x_train, np.array(y_lable))
recognizer.save("training_data.yml")