#!/bin/python3

from Canopto import Canopto
import pygame
from pygame.locals import *
import time
import random
from colorsys import *

c = Canopto(2, 8, False)
c.bs.clear()

while True:
	last_x = 0
	for y in range(0, 8):
		if y > 0:
			# Write new position as a white snowflake
			x = random.randint(0, c.width-1)
			c.setPixel(x, y, (255, 255, 255))
			# Fade out old position
			while c.getPixel(last_x, y-1)[0] > 0:
				fading_color=rgb_to_hls(*(v / 255.0 for v in c.getPixel(last_x, y-1)))
				fading_color = (fading_color[0],(fading_color[1] - 0.03),fading_color[2]);
				print (fading_color)
				fading_color= (hls_to_rgb(*fading_color)[0]*255.0, hls_to_rgb(*fading_color)[1]*255.0, hls_to_rgb(*fading_color)[2]*255.0)
				c.setPixel(x, y-1, fading_color)
				time.sleep(0.02)
			last_x = x
	time.sleep(3)
		
	# Create a 1-pixel white snowflake
	# Animate it falling down, by moving the snowflake to a random column, and fading out previoud position