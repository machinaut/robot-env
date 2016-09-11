#!/usr/bin/env python

import sys
import serial
import pygame
from pygame.locals import *

# [forward_key, zero_key, backwards_key]
base_keys 	= [K_q, K_a, K_z]
shoulder_keys 	= [K_w, K_s, K_x]
elbow_keys 	= [K_e, K_d, K_c] 
wrist_keys 	= [K_r, K_f, K_v]
grip_keys 	= [K_t, K_g, K_b]

# Loop time delay in ms
steptime = 10

# Move per step
servomv = 1

servocenter = 0

pygame.init()
display = pygame.display.set_mode((100,100))

#ser = serial.Serial(	port = sys.argv[1],
#			baudrate = 115200,
#			parity = serial.PARITY_NONE,
#			stopbits = serial.STOPBITS_ONE,
#			bytesize = serial.EIGHTBITS)

ser = serial.Serial(sys.argv[1],115200) 
b_pos = 90
s_pos = 90 
e_pos = 90
w_pos = 90
g_pos = 90

def pos_normalize():
	global b_pos, s_pos, e_pos, w_pos, g_pos
	b_pos = max(0, min(b_pos, 180))
	s_pos = max(0, min(s_pos, 180))
	e_pos = max(0, min(e_pos, 180))
	w_pos = max(0, min(w_pos, 180))
	g_pos = max(0, min(g_pos, 180))

while 1:
	pygame.event.pump()
	
	# Make it quits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
		ser.close()
                pygame.quit(); sys.exit();
	
	print ser.readline()

	keys = pygame.key.get_pressed()

	if keys[base_keys[0]]:
		b_pos += servomv
	if keys[base_keys[1]]:
		b_pos = servocenter
	if keys[base_keys[2]]:
		b_pos -= servomv
	
	if keys[shoulder_keys[0]]:
		s_pos -= servomv
	if keys[shoulder_keys[1]]:
		s_pos = servocenter
	if keys[shoulder_keys[2]]:
		s_pos += servomv

	if keys[elbow_keys[0]]:
		e_pos += servomv
	if keys[elbow_keys[1]]:
		e_pos = servocenter
	if keys[elbow_keys[2]]:
		e_pos -= servomv

	if keys[wrist_keys[0]]:
		w_pos += servomv
	if keys[wrist_keys[1]]:
		w_pos = servocenter
	if keys[wrist_keys[2]]:
		w_pos -= servomv

	if keys[grip_keys[0]]:
		g_pos += servomv
	if keys[grip_keys[1]]:
		g_pos = servocenter
	if keys[grip_keys[2]]:
		g_pos -= servomv

	pygame.time.wait(steptime)
	
	pos_normalize()
	
        cmd_str = ','.join([str(b_pos), str(s_pos), str(e_pos), str(w_pos), str(g_pos)])
	cmd_str = 'W' + cmd_str + '\n'
	print cmd_str
	ser.write(cmd_str)
	ser.flush()
