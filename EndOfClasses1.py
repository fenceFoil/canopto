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
import text

display_size = (8, 8)
cans = Canopto (display_size[0], display_size[1], True, True)

def scrollRainbowText (canopto, text, font = "16bfZX", yOffset = 2, speed = 1.2):
	#TinyUnicode 16, offset 5
	#Habbo 12, offset 0
	#16bfZX 16, offset 2
	gold_color = Color(0, 0, 0, 0)
	gold_color.hsla = (50, 100, 50, 100)
	green_color = Color(0, 0, 0, 0)
	green_color.hsla = (88 + (104 - 88) * 0.8, 100, 50, 100)
	
	colors = [green_color, gold_color]
	
	surface = pygame.font.Font(font+".ttf", 16).render(text, False, (0xff, 0xff, 0xff), (0x00, 0x00, 0x00))
	color = 0
	lastColor = color
	for x in range (0, surface.get_width()-(canopto.width-1)):
		if (x % 12 == 0):
			color = (color + 1) % len(colors)
		
		if (color != lastColor):
			surface = pygame.font.Font(font+".ttf", 16).render(text, False, colors[color], (0x00, 0x00, 0x00))
			lastColor = color
		frame = Surface ((canopto.width, canopto.height))
		frame.blit (surface, (-x, -yOffset))
		canopto.drawSurface(frame)
		
		canopto.update()
		for event in pygame.event.get():
			if event.type==QUIT:
				sys.exit(0)
		time.sleep(((1/speed) * 0.07))

# scroll text across canopto. blocks. fg & bg are colors
def scrollText (canopto, text, fg = (0xFF, 0x33, 0xFF), bg = (0x00, 0x00, 0x00, 0x00), font = "16bfZX", yOffset = 2, speed = 1.2):
	#TinyUnicode 16, offset 5
	#Habbo 12, offset 0
	#16bfZX 16, offset 2
	#surface = pygame.font.SysFont("16bfZX", 16).render(text, False, fg, bg)
	surface = pygame.font.Font(font+".ttf", 16).render(text, False, fg, bg)
	scrollSurface(canopto, surface, speed, yOffset = 2)

# speed is a multiplier of the default speed which is pretty good. Blocks until
# surface has finished scrolling
def scrollSurface (canopto, surface, speed = 1, yOffset = 0):
	for x in range (0, surface.get_width()-(canopto.width-1)):
		frame = Surface ((canopto.width, canopto.height))
		frame.blit (surface, (-x, -yOffset))
		canopto.drawSurface(frame)
		
		canopto.update()
		for event in pygame.event.get():
			if event.type==QUIT:
				sys.exit(0)
		time.sleep((1/speed) * 0.07)

old_image = Surface(display_size)
while True:
	scrollRainbowText(cans, "   We Did It Fam!   ", speed = 1.2)
	time.sleep(2)