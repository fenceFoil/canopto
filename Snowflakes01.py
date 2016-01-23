#!/bin/python3

from Canopto import Canopto
import pygame
from pygame.locals import *
import time
import random
from colorsys import *

c = Canopto(2, 8, False)
c.bs.clear()
c.bs.send_data(0)

while True:
	x = random.randint(0, c.width-1)
	last_x = x
	for y in range(0, c.height):
		# Write new position as a white snowflake
		#x = random.randint(0, c.width-1)
		c.setPixel(x, y, (255, 255, 255))
		if y > 0:
			# Fade out old position
			while c.getPixel(last_x, y-1)[0] > 0:
				fading_color=rgb_to_hls(*(v / 255.0 for v in c.getPixel(last_x, y-1)))
				fading_color = (fading_color[0],max(fading_color[1] - 0.03, 0),fading_color[2])
				fading_color= (hls_to_rgb(*fading_color)[0]*255.0, hls_to_rgb(*fading_color)[1]*255.0, hls_to_rgb(*fading_color)[2]*255.0)
				print (fading_color)
				c.setPixel(last_x, y-1, fading_color)
				time.sleep(0.02)
			last_x = x
	time.sleep(3)
	
	c.setPixel(x, c.height
		
	# Create a 1-pixel white snowflake
	# Animate it falling down, by moving the snowflake to a random column, and fading out previoud position