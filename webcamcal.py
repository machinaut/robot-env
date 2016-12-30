#!/usr/bin/env python
import sys
import numpy as np
import cv2

def nothing(x):
    print('got x', x)

# Grab webcam number from first command line argument
try:
    dev = int(sys.argv[1])
except:
    raise Exception("The first arg to this program should be\
an integer that tells it what camera to use")

# Get the webcam setup to use
cap = cv2.VideoCapture(dev)
cv2.namedWindow('frame')

######## Setup everything ahead of time for our calibration ########
bsize = (5,4)
objpsz = bsize[0]*bsize[1]
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((objpsz,3), np.float32)
objp[:,:2] = np.mgrid[0:bsize[0],0:bsize[1]].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


while(True):
    # Capture frame-by-frame
    _, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, bsize,
            cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print "FOUND!!"
        print corners
        print "\n"
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(frame, bsize, corners2,ret)
    else:
        img = frame
 
    # Display the resulting frame
    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if len(objpoints) >= 15:
        break

if len(objpoints) < 15:
    print "Not enough calibration data!"
else:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    print 'ret', ret
    print 'mtx', mtx
    print 'dist', dist
    print 'rvecs', rvecs
    print 'tvecs', tvecs

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
