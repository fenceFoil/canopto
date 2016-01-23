#!/bin/python3
import blinkstick.blinkstick
import pygame
from pygame.locals import *
import time
import numpy

#Blinkstick init
bs = blinkstick.blinkstick.BlinkStickPro (16, 0, 0, 0.002, 255)
bs.connect()

#Pygame init
pygame.init()
SCREEN = pygame.display.set_mode((500,400),0,32)
BLACK = (0,0,0)
WHITE = (255,255,255)


class Canopto:
	'The Matrix of LEDs that make up the display'
	colCount = 2
	rowCount = 8
	matrix = numpy.zeros((rowCount,colCount), dtype=(float,3))
	pixelPadding = 10
	pyCenter = (int(SCREEN.get_width()/2), int(SCREEN.get_height()/2))
	
	def __init__(self, colCount, rowCount, bs, pg):
		print("Initializing...")
		self.bs = bs
		self.pg = pg
	
	def writeChar(self, character):
		'Write the character to the display'
		print("Wrote Char " + character)
	
	def update(self):
		#print matrix to console
		print(self.matrix)
		
		#reset pygame window
		SCREEN.fill(BLACK)
		
		#draw pixels onto pygame window
		for r in range(0,self.rowCount):
			for c in range(0,self.colCount):
				#~ self.pg
				pygame.draw.circle(SCREEN, WHITE, (c*20 + 100, r*20 + 100), 10)
		#~ self.pg
		pygame.display.update()
		
	def softToHardPixel(self, row, col):
		'Convert a software pixel (row, col) to the hardware pixel index'
		print("UGGH")
		
	def setPixel(self, row, col, color):
		self.matrix[row][col] = color
		bs.set_color (0, 1, color[0], color[1], color[2])
		bs.send_data(0)




CANOPTO = Canopto(2, 8, bs, pygame)
CANOPTO.setPixel(0,0, WHITE)
while 1:
	CANOPTO.update()
	
	time.sleep(.25)
