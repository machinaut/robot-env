#!/usr/bin/env python
import sys
import numpy as np
import cv2
import datetime
import time

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

#cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, 800)
#cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 600)

######## Setup everything ahead of time for our calibration ########
bsize = (6,9)
objpsz = bsize[0]*bsize[1]
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((objpsz,3), np.float32)
objp[:,:2] = np.mgrid[0:bsize[0],0:bsize[1]].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

dtstart = datetime.datetime.today().strftime('%Y-%m-%d-%H%M%S')
i = 0
enable = True
nextcap = time.time()
while(True):
    # Capture frame-by-frame
    _, frame = cap.read()
    #blr = 3
    #blur = cv2.GaussianBlur(frame, (blr,blr), 0)
    blur = frame
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    #opts =  cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_FAST_CHECK  
    opts = cv2.CALIB_CB_FAST_CHECK  
    ret, corners = cv2.findChessboardCorners(gray, bsize, opts)

    # If found, add object points, image points (after refining them)
    if (ret == True) and (enable == True):
        print "FOUND!!"
        print corners
        print "\n"
        objpoints.append(objp)

        cv2.imwrite("{}_found_board_{}.png".format(dtstart,i), gray)
        i += 1
        
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(frame, bsize, corners2,ret)
        enable = False
        nextcap = time.time() + 2
    else:
        img = frame
 
    if time.time() >= nextcap:
        enable = True

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
    datetime = datetime.datetime.today().strftime('%Y-%m-%d-%H%M%S')
    np.savez('./camera_cal_{}'.format(datetime), ret=ret, mtx=mtx, dist=dist,
            rvecs=rvecs, tvecs=tvecs)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
