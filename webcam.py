#!/usr/bin/env python
import numpy as np
import cv2

blursize = 55

vc = cv2.VideoCapture(1)

# Orange?  These are HSV values.
color_min = np.array([7,50,50], np.uint8)
color_max = np.array([12,255,255], np.uint8)

while True:
  _, im = vc.read()
  cv2.imshow('hi', im)
  # Apply a gaussian blur to the whole image
  cv2.GaussianBlur(im, (blursize,blursize), 0)
  # Convert to HSV colorspace for easier color-based thresholding
  hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
  # Threshold based on given min/max - restrictive in hue but generous in saturation/value
  thresh = cv2.inRange(hsv, color_min, color_max)
  cv2.imshow('yo', thresh)

  cv2.waitKey(1)
