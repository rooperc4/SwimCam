import numpy as np
import cv2 as cv
cap0 = cv.VideoCapture(0)
cap1 = cv.VideoCapture(2)
if not cap0.isOpened():
    print("Cannot open camera 0")
    exit()
if not cap1.isOpened():
    print("Cannot open camera 1")
    exit()
while True:
    # Capture frame-by-frame
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()
    # if frame is read correctly ret is True
    if not ret1:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
#    gray0 = cv.cvtColor(frame0, cv.COLOR_BGR2GRAY)
#    gray1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame1', frame1)
    cv.imshow('frame0', frame0)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap0.release()
cap1.release()
cv.destroyAllWindows()
