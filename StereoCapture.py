import numpy as np
import cv2 as cv
from datetime import datetime
import os
import os.path as path

os.chdir("Data")
date1=datetime.now().strftime('D%Y%m%d-T%H%M%S')
os.mkdir(date1)
os.chdir(date1)
os.mkdir("images")
os.mkdir("logs")
os.mkdir("settings")

os.mkdir("images/right")
os.mkdir("images/left")

right_dir="./images/right"
left_dir="./images/left"
EXTENSION="jpg"
right_name="R_IMX322USB"
left_name="L_IMX322USB" 
frame_interval=1000

file_name_format="{:05d}_D{:s}_{:s}.{:s}"
cap = cv.VideoCapture(0)
cap1 = cv.VideoCapture(2)

frame_count = 0

while(True):
    frame_count += 1
    for x in range(4):
        ret, frame = cap.read()
        ret1, frame1 = cap1.read()

    ret, frame = cap.read()
    ret1, frame1 = cap1.read()

    cv.imshow('frame',frame)  #show all frames
    cv.imshow('frame1', frame1)

    date=datetime.now().strftime('%Y%m%d-T%H%M%S.%f')[:-3]
    file_name=file_name_format.format(frame_count,date,right_name,EXTENSION)
    file_path=path.normpath(path.join(right_dir,file_name))
    cv.imwrite(file_path, frame) #write specific frames 

    date=datetime.now().strftime('%Y%m%d-T%H%M%S.%f')[:-3]
    file_name=file_name_format.format(frame_count,date,left_name,EXTENSION)
    file_path=path.normpath(path.join(left_dir,file_name))
    cv.imwrite(file_path, frame1)

    if cv.waitKey(frame_interval) & 0xFF == ord('q'):
        break


cv.destroyAllWindows()
