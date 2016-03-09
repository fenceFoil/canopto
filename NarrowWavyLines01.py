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
cans = Canopto (display_size[0], display_size[1], True, True)

# Create an image, wider than the display, with randomized lines across it 
# and a little buffer to each side
# Scroll image over display

while True:
	# Make an image 1000 pixels wide
	lines = Surface((1000, display_size[1]+2))
	lines.fill(Color(0, 0, 92, 255))
	
	# Draw lines
	# Come up with sets of points. Alternate between high and low lines. Allow random space between each, and generate up to the end of the surface
	
	# Simple algorithm: generate one line. 
	margin = 5
	currX = margin
	points = [(margin, randint(0, lines.get_height()-1))]
	while currX < lines.get_width() - margin:
		currX = randint(currX+7, currX+30)
		currX = min(lines.get_width()-margin, currX)
		points.append ((currX, randint(1, lines.get_height()-2)))
		
	# Draw line from points
	#line_color = Color(54, 255, 54, 255)
	line_color = Color(255, 128, 0, 255)
	pygame.draw.aalines(lines, line_color, False, points)
	
	# Scroll image across canopto
	for x in range (0, lines.get_width()-(display_size[0]-1)):
		frame = Surface (display_size)
		frame.blit (lines, (-x, -1))
		cans.drawSurface(frame)
		
		cans.update()
		for event in pygame.event.get():
			if event.type==QUIT:
				sys.exit(0)
		time.sleep(0.03)