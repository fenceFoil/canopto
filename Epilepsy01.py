#!/bin/python3

from Canopto import Canopto
import pygame
from pygame import *
from pygame.locals import *
import time
from random import randint
from colorsys import *
import sys

display_size = (4, 8)
cans = Canopto (display_size[0], display_size[1], False, True)

# Create image of random colors with a constant lightness
# Fade it over the previous image
# Delay
# Repeat forever

colors = [Color(0, 0, 0, 255), Color(0, 255, 255, 0)]
curr_color = 0
cycle_fwd = True
while True:
	new_image = Surface(display_size)
	new_image.fill(colors[curr_color])
	
	hue = colors[1].hsla[0]
	if (cycle_fwd):
		hue = (hue + 2)
		if (hue >= 360):
			cycle_fwd = False
			hue = 359
	else:
		hue = hue - 2
		if (hue < 0):
			hue = 0
			cycle_fwd = True
	colors[1].hsla = (hue, 100, 50, 100)
	
	cans.drawSurface(new_image)
		
	cans.update()
	for event in pygame.event.get():
		if event.type==QUIT:
			sys.exit(0)
	time.sleep(0.06)
	
	curr_color = (curr_color+1) % len(colors)