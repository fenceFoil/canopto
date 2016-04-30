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
from itertools import chain

display_size = (8, 8)
cans = Canopto (display_size[0], display_size[1], True, True)

def get_window_at_pos (baseImage, pos, windowSize=display_size):
	return baseImage.subsurface(((baseImage.get_width() - windowSize[0])*pos[0], (baseImage.get_height() - windowSize[1])*pos[1]), windowSize)

base_image = pygame.image.load("res/picture.png")

# Zoom in on a position within a larger image slowly
# Zoom back out
# Repeat with a new position

old_image = Surface(display_size)
while True:
	# Zoom in and out again
	pos = (random(), random())
	
	steps = 100
	for x in chain(
			tween(easeInOutCubic, 0, steps/7, steps, True, False), 
			tween(easeInOutCubic, steps/7, 0, steps, True, False)):
		
		zoom = x / float(steps);
		frame = get_window_at_pos (smoothscale(base_image, (round((base_image.get_width()-display_size[0]) * zoom + display_size[0]), round((base_image.get_height()-display_size[1]) * zoom + display_size[1]))), pos)

		cans.drawSurface(frame)
		cans.update()
		for event in pygame.event.get():
			if event.type==QUIT:
				sys.exit(0)
		time.sleep(1/float(steps))