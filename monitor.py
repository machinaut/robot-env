#!/usr/bin/env python
# monitor.py - dumb serial port monitor for debugging
import serial
ser = serial.Serial('/dev/ttyUSB0', 115200)
while True:
  print(ser.readline().strip())
