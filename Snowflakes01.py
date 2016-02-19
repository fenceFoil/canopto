#!/bin/python3

from Canopto import Canopto
import pygame
from pygame.locals import *
import time
import random
from colorsys import *

c = Canopto(4, 8, True, True)
c.bs.clear()
c.bs.send_data(0)

while True:
	x = random.randint(0, c.width-1)
	last_x = x
	for y in range(0, c.height+1):
		# Write new position as a white snowflake
		#x = random.randint(0, c.width-1)
		if y < c.height:
			c.setPixel(x, y, (255, 255, 255))
			
		fade_time = 0.75
		if y > 0:
			# Fade out old position
			fade_step = 0.02
			old_pos_color = (1, 1, 0)
			while c.getPixel(last_x, y-1)[0] > 0:
				old_pos_color = (old_pos_color[0], max(old_pos_color[1] - 0.03, 0), old_pos_color[2])
				fading_color = (hls_to_rgb(*old_pos_color)[0]*255.0, hls_to_rgb(*old_pos_color)[1]*255.0, hls_to_rgb(*old_pos_color)[2]*255.0)
				c.setPixel(last_x, y-1, fading_color)
				time.sleep(fade_time * fade_step)
			last_x = x
		else:
			time.sleep(fade_time)
	#time.sleep(3)
	
	c.setPixel(x, c.height-1, (0, 0, 0))
		
	# Create a 1-pixel white snowflake
	# Animate it falling down, by moving the snowflake to a random column, and fading out previoud position