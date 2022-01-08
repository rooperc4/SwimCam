import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)
#cap.set(cv.CAP_PROP_FOURCC,cv.VideoWriter_fourcc('M','J','P','G'))
cap1 = cv.VideoCapture(2)
#cap1.set(cv.CAP_PROP_FOURCC,cv.VideoWriter_fourcc('M','J','P','G'))

while(True):
 #   gps.update()
  #  frame_count += 1
    for x in range(4):
        ret, frame = cap.read()
        ret1, frame1 = cap1.read()

    ret, frame = cap.read()
    ret1, frame1 = cap1.read()

    cv.imshow('frame',frame)  #show all frames
 #   cv.imshow('frame1', frame1)
