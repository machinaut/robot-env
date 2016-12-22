#!/usr/bin/env python
import sys
import numpy as np
import cv2

def nothing(x):
    print('got x', x)

try:
    dev = int(sys.argv[1])
except:
    raise Exception("The first arg to this program should be\
an integer that tells it what camera to use")

cap = cv2.VideoCapture(dev)
cv2.namedWindow('frame')

arudict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

distcoef = np.array([[0.06665446, -0.1910065, 0.00630647, 0.01302178, 0.15293528]])
cammat = np.array([[1.65211157e+03, 0.00000000e+00, 1.02022795e+03],
         [0.00000000e+00, 1.65353664e+03, 5.59629568e+02],
          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

while(True):
    # Capture frame-by-frame
    _, frame = cap.read()
    # Blur the image to smooth everything over
    #blur = cv2.GaussianBlur(img, (5, 5), 0)
    # Convert to grayscale because we don't need color for edge detection
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    corners, ids, _ = cv2.aruco.detectMarkers(frame, arudict)
    frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    
    try:
        myids = [e[0] for e in ids]
    except:
        myids = []

    rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(corners, 0.070, cammat, distcoef)
    
    if len(myids) == 2:
        dist = np.linalg.norm(tvecs[0]-tvecs[1])
        print dist

    try:
        for rvec, tvec in zip(rvecs, tvecs):
            frame = cv2.aruco.drawAxis(frame, cammat, distcoef, rvec, tvec, 0.070)
    except:
        pass

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
