#!/bin/python3

from Canopto import Canopto
import pygame
from pygame import *
from pygame.locals import *
import time
from random import randint
from random import random
from colorsys import *
import sys

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
			color_index = random()
		
			rand_color = Color(0, 0, 0, 0)
			rand_color.hsla = (40 + (x+y*8)*2, 100, max(50-50*color_index, 5), 100)
			#rand_color.hsla = (max(40, 20+(60+40)*color_index), 100, max(50-50*color_index, 5), 100)
			new_image.set_at((x, y), rand_color)
	
	# Fade onto old image
	for alpha in range (0, 256, 12):
		intermediate_image = old_image.copy()
		new_image.set_alpha(alpha)
		intermediate_image.blit(new_image, (0, 0))
		cans.drawSurface(intermediate_image)
		
		cans.update()
		for event in pygame.event.get():
			if event.type==QUIT:
				sys.exit(0)
		time.sleep(0.02)
		
	time.sleep(0.12)
	
	new_image.set_alpha(255)
	old_image = new_image