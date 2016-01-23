#!/bin/python3
import blinkstick.blinkstick as blinkstick
import pygame
from pygame.locals import *
import time
import numpy

BLACK = (0,0,0)
WHITE = (255,255,255)

class Canopto:
	'The Matrix of LEDs that make up the display'
	width = 2
	height = 8
	matrix = numpy.zeros((height,width), dtype=(float,3))
	pixelPadding = 10
	# pyCenter = (int(self.self.SCREEN.get_width()/2), int(selfSCREEN.get_height()/2))
	
	def __init__(self, width, height):
	
		#Only works for 1 column
		if (width > 2):
			print("!!!!WARNING: UNSUPPORTED NUMBER OF COLUMNS!!!")
		
		#Blinkstick init
		self.bs = blinkstick.BlinkStickPro (width*height, 0, 0, 0.002, 255)
		self.bs.connect()
		#self.bs.set_mode(2)

		#Pygame init
		pygame.init()
		self.SCREEN = pygame.display.set_mode((500,400),0,32)

	
	def writeChar(self, character):
		'Write the character to the display'
		print("Wrote Char " + character)
	
	def update(self):
		#print matrix to console
		print(self.matrix)
		
		#reset pygame window
		self.SCREEN.fill(BLACK)
		
		#draw pixels onto pygame window
		for r in range(0,self.height):
			for c in range(0,self.width):
				#~ self.pg
				pygame.draw.circle(self.SCREEN, WHITE, (c*20 + 100, r*20 + 100), 10)
		#~ self.pg
		pygame.display.update()
		
	def softToHardPixel(self, col, row):
		'Convert a software pixel (col, row) to the hardware pixel index'
		print("UGGH")
		# 16 or width*height*(col//2) selects a 2-can-wide column of lights
		# (((height-1)-row)//4) selects a cell of 4 cans
		# (row%2) adds one if the row is odd
		# (col%2) is true for the second column of cans in a cell
		# (1+((row+1)%2)) adds 1 for the lower right can in a cell, and adds one more for the upper right can in a cell
		return (self.width*self.height)*(col//2) + (((self.height-1)-row)//2)*4+(row%2)+(col%2)*(3-2*((row)%2))		
	def setPixel(self, col, row, color):
		self.matrix[row][col] = color
		print (self.softToHardPixel(col, row))
		self.bs.set_color (0, self.softToHardPixel(col, row), color[0], color[1], color[2])
		self.bs.send_data(0)


#Main
if __name__ == "__main__":
	CANOPTO = Canopto(2, 8)
	for i in range(0, 2):
		CANOPTO.setPixel(0, i, (0, 255, 0))
	while False:
		CANOPTO.update()
		
		time.sleep(1)
