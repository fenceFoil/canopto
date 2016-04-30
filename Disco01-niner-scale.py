#!/bin/python3

from Canopto import Canopto
import pygame
from pygame import *
from pygame.locals import *
from pygame.transform import *
import time
from random import randint
from random import random
from colorsys import *
import sys
from tween import *

display_size = (8, 8)
cans = Canopto (display_size[0], display_size[1], True, True)

# Create image of random colors with a constant lightness
# Fade it over the previous image
# Delay
# Repeat forever

old_image = Surface(display_size)
while True:
	new_image = Surface(display_size)
	for x in range (0, display_size[0]):
		for y in range (0, display_size[1]):
			# Show either gold or a random green
			rand_color = Color(0, 0, 0, 0)
			if (random() > 0.9):
				rand_color.hsla = (50, 100, 50, 100)
			else:
				# Green
				brightness = 10
				if (random() > 0.4):
					brightness = 28
				rand_color.hsla = (88 + (104 - 88) * random(), 100, brightness, 100)
			
			new_image.set_at((x, y), rand_color)
	
	# Fade onto old image
	steps = 30
	for alpha in tween(easeInOutSine, 0,255,steps,True,False):
		intermediate_image = old_image.copy()
		new_image.set_alpha(alpha)
		intermediate_image.blit(new_image, (0, 0))
		cans.drawSurface(smoothscale(intermediate_image, (display_size[0]*2, display_size[1]*2)))
		
		cans.update()
		for event in pygame.event.get():
			if event.type==QUIT:
				sys.exit(0)
		time.sleep(0.9/steps)
		
	#time.sleep(0.12)
	
	new_image.set_alpha(255)
	old_image = new_image