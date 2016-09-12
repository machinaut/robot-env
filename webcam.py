#!/usr/bin/env python
import numpy as np
import cv2

blursize = 21

vc = cv2.VideoCapture(1)

# Orange?  These are HSV values.
color_min = np.array([7,50,50], np.uint8)
color_max = np.array([12,255,255], np.uint8)

# detector
params = cv2.SimpleBlobDetector_Params()
params.filterByColor = False
params.filterByConvexity = False
params.filterByCircularity = False
params.filterByInertia = False
params.filterByArea = True
params.minArea = 100
params.maxArea = 10000
detector = cv2.SimpleBlobDetector(params)

while True:
  _, im = vc.read()
  cv2.imshow('hi', im)
  # Apply a gaussian blur to the whole image
  cv2.GaussianBlur(im, (blursize,blursize), 0)
  # Convert to HSV colorspace for easier color-based thresholding
  hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
  # Threshold based on given min/max - restrictive in hue but generous in saturation/value
  thresh = cv2.inRange(hsv, color_min, color_max)
  # Gaussian again for good measure
  cv2.GaussianBlur(thresh, (blursize, blursize), 0)
  cv2.imshow('yo', thresh)
  M = cv2.moments(thresh)
  cx = int(M['m10']/M['m00'])
  cy = int(M['m01']/M['m00'])
  print('moments',cx,cy)

  cv2.waitKey(1)
