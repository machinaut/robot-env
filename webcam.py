#!/usr/bin/env python
import cv2

vc = cv2.VideoCapture(1)

while True:
  _, im = vc.read()
  cv2.imshow('hi', im)
  cv2.waitKey(1)
