#!/bin/python3
import blinkstick.blinkstick as blinkstick
import pygame
from pygame.locals import *
import time
import numpy
from random import randint

BLACK = (0,0,0)
WHITE = (255,255,255)

class Canopto:
	'The Matrix of LEDs that make up the display'
	
	
	def __init__(self, width = 2, height = 8, simulatorEnabled = True):
		self.width = width
		self.height = height
		self.simulatorEnabled = simulatorEnabled
		self.matrix = numpy.zeros((self.height, self.width), dtype=(float,3))
		
		#Only works for 1 xumn
		if (width > 2):
			print("!!!!WARNING: UNSUPPORTED NUMBER OF xUMNS!!!")
		
		#Blinkstick init
		self.bs = blinkstick.BlinkStickPro (width*height, 0, 0, 0.002, 255)
		self.bs.connect()
		#self.bs.set_mode(2)

		if self.simulatorEnabled:
			#Pygame init
			pygame.init()
			self.SCREEN = pygame.display.set_mode((400,400),0,32)

	
	def writeChar(self, character):
		'Write the character to the display'
		print("Wrote Char " + character)
	
	def update(self):
		#print matrix to console
		print(self.matrix)
		
		
		
		#draw pixels onto pygame window
		if self.simulatorEnabled:
			#reset pygame window
			self.SCREEN.fill(BLACK)
		
			for y in range(0,self.height):
				for x in range(0,self.width):
					#Draw circular pixels
					pygame.draw.circle(self.SCREEN, self.matrix[y][x], (x*20 + 100, y*20 + 100), 10)
					
					#Draw pixel boundaries
					borderRect = pygame.Rect((x*20 + 90, y*20 + 90), (20, 20))
					pygame.draw.rect(self.SCREEN, ([75] * 3), borderRect, 1)
			#update the screen!
			pygame.display.update()
		
		
	def softToHardPixel(self, x, y):
		'Convert a software pixel (x, y) to the hardware pixel index'
		# 16 or width*height*(x//2) selects a 2-can-wide xumn of lights
		# (((height-1)-y)//4) selects a cell of 4 cans
		# (y%2) adds one if the y is odd
		# (x%2) is true for the second xumn of cans in a cell
		# (1+((y+1)%2)) adds 1 for the lower right can in a cell, and adds one more for the upper right can in a cell
		return (self.width*self.height)*(x//2) + (((self.height-1)-y)//2)*4+(y%2)+(x%2)*(3-2*((y)%2))		
		
	def setPixel(self, x, y, color):
		self.matrix[y][x] = color
		print (self.softToHardPixel(x, y))
		self.bs.set_color (0, self.softToHardPixel(x, y), color[0], color[1], color[2])
		self.bs.send_data(0)
	
	def randomColor(self):
		return (randint(0,255), randint(0,255), randint(0,255))


#Main
if __name__ == "__main__":
	CANOPTO = Canopto(2, 8, simulatorEnabled = True)
	while True:
		print(CANOPTO.matrix)
		randomX = randint(0,CANOPTO.width-1)
		randomY = randint(0,CANOPTO.height-1)		
		CANOPTO.setPixel(randomX, randomY, CANOPTO.randomColor())
		CANOPTO.update()
		time.sleep(1)
