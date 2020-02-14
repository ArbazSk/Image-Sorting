import os
import numpy as np
import cv2

filename = "video.avi"
fps = 24.0
res = '480p'


# set resolution 
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

def get_dim(cap, res='720p'):
    width, height = STD_DIMENSIONS['480p']
    if res in STD_DIMENSIONS:
         width, height = STD_DIMENSIONS[res]
    
    # change the resolution to given resolution
    change_res(cap, width, height)

    return width, height


# video encodeing
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}
def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

cap = cv2.VideoCapture(0)
dim = get_dim(cap, res=res)
video_type = get_video_type(filename)

out = cv2.VideoWriter(filename, video_type, fps, dim)

while(True):
    ret, frame = cap.read()
    
    out.write(frame) # will write the  frames into memory

    cv2.imshow('Frame', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
    