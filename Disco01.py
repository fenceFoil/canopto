#!/bin/python3

from Canopto import Canopto
from pygame import *
from pygame.locals import *
import time
from random import randint
from colorsys import *

display_size = (2, 8)
cans = Canopto (display_size[0], display_size[1], False, True)

# Create image of random colors with a constant lightness
# Fade it over the previous image
# Delay
# Repeat forever

old_image = Surface(display_size)
while True:
	new_image = Surface(display_size)
	for x in range (0, 2):
		for y in range (0, 8):
			rand_color = Color(0, 0, 0, 0)
			rand_color.hsla = (randint(0, 360), 100, 50, 100)
			new_image.set_at((x, y), rand_color)
	
	# Fade onto old image
	for alpha in range (0, 256, 4):
		intermediate_image = old_image.copy()
		new_image.set_alpha(alpha)
		intermediate_image.blit(new_image, (0, 0))
		cans.drawSurface(intermediate_image)
		
		time.sleep(0.02)
	
	new_image.set_alpha(255)
	old_image = new_image