#!/bin/python3

import Canopto
import pygame
from pygame.locals import *
import time
import random

c = Canopto(2, 8)

while True:
	last_x = 0
	for y in range(0, 8):
		if y > 0:
			# Fade out old position
			while c.get
			last_x
		
	# Create a 1-pixel white snowflake
	# Animate it falling down, by moving the snowflake to a random column, and fading out previoud position