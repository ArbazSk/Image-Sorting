import cv2
import os
import numpy as np
from collections import Counter

def object_det(directory, filename):
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

		# make_dir_path = os.path.join("f:/",keysList[0])
		# if os.path.exists(make_dir_path):
		# 	move_to_folder(directory,filename,make_dir_path)
		# c
		return keysList[0]
