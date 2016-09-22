#!/usr/bin/env python

import sys
import serial
import pygame
from pygame.locals import *

DBG = True

#Dicts everywhere
axis_data = {'base' : {'upkey':K_q, 'zerokey':K_a, 'downkey':K_z, 'pos':90},
             'shoulder' : {'upkey':K_x, 'zerokey':K_s, 'downkey':K_w, 'pos':90},
             'elbow' : {'upkey':K_e, 'zerokey':K_d, 'downkey':K_c, 'pos':90},
             'wrist' : {'upkey':K_r, 'zerokey':K_f, 'downkey':K_v, 'pos':90},
             'grip' : {'upkey':K_t, 'zerokey':K_g, 'downkey':K_b, 'pos':90}}

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

servocenter = 90

pygame.init()
display = pygame.display.set_mode((100,100))

#ser = serial.Serial(	port = sys.argv[1],
#			baudrate = 115200,
#			parity = serial.PARITY_NONE,
#			stopbits = serial.STOPBITS_ONE,
#			bytesize = serial.EIGHTBITS)

if not DBG:
	ser = serial.Serial(sys.argv[1],115200) 

b_pos = 90
s_pos = 90 
e_pos = 90
w_pos = 90
g_pos = 90

def dict_normalize():
	global axis_data
	for axis in axis_data.iteritems():
		name = axis[0]
		axis = axis[1]
		axis['pos'] = max(0, min(axis['pos'], 180))

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
		if not DBG:
			ser.close()
                pygame.quit(); sys.exit();
	
	if not DBG:
		print ser.readline()

	keys = pygame.key.get_pressed()
	
	for axis in axis_data.iteritems():
		axisname = axis[0]
		axis = axis[1]
		if keys[axis['upkey']]:
			axis['pos'] += servomv
		if keys[axis['zerokey']]:
			axis['pos'] = servocenter
		if keys[axis['downkey']]:
			axis['pos'] -= servomv
		#print axisname, axis	

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
	dict_normalize()
        
	cmd_str2 = ','.join([str(axis_data[ax]['pos']) for ax in ['base', 'shoulder', 'elbow', 'wrist', 'grip']])
	cmd_str2 = 'W' + cmd_str2 + '\n'
	
	cmd_str = ','.join([str(b_pos), str(s_pos), str(e_pos), str(w_pos), str(g_pos)])
	cmd_str = 'W' + cmd_str + '\n'
	if DBG:
		print cmd_str
		print cmd_str2
	else:
		ser.write(cmd_str)
		ser.flush()
