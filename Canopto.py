#!/bin/python3
import blinkstick.blinkstick as blinkstick
import pygame
from pygame.locals import *
import time
import numpy
from random import randint
import pygame.surfarray as surfarray

BLACK = (0,0,0)
WHITE = (255,255,255)

class Canopto:
	'The Matrix of LEDs that make up the display'
	
	def __init__(self, width = 2, height = 8, previewEnabled = True, useGamma = False, backgroundColor = (50,50,50), fontColor = (255, 255, 255)):
		self.width = width
		self.height = height
		self.previewEnabled = previewEnabled
		self.useGamma = useGamma
		self.matrix = numpy.zeros((self.height, self.width), dtype=(float,3))
		
		self.gamma = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
		1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4,
		4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9,
		10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
		17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25, 25,
		26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36, 37, 38,
		39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50, 51, 52, 54,
		55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68, 69, 70, 72, 73,
		74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89, 90, 92, 93, 95, 96,
		98, 99, 101, 102, 104, 105, 107, 109, 110, 112, 114, 115, 117, 119,
		120, 122, 124, 126, 127, 129, 131, 133, 135, 137, 138, 140, 142,
		144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 167, 169,
		171, 173, 175, 177, 180, 182, 184, 186, 189, 191, 193, 196, 198,
		200, 203, 205, 208, 210, 213, 215, 218, 220, 223, 225, 228, 231,
		233, 236, 239, 241, 244, 247, 249, 252, 255 ]
		
		#Colors
		self.backgroundColor = self.toGamma(backgroundColor)
		self.fontColor = self.toGamma(fontColor)
		
		#Only works for 1 column
		if (width > 2):
			print("!!!!WARNING: UNSUPPORTED NUMBER OF COLUMNS!!!")
		
		#Blinkstick init
		self.bs = blinkstick.BlinkStickPro (width*height, 0, 0, 0.002, 255)
		self.bs.connect()
		#self.bs.set_mode(2)

		pygame.init()
		self.clock = pygame.time.Clock()
		if self.previewEnabled:
			#Pygame init
			self.SCREEN = pygame.display.set_mode((400,400),0,32)
			
		self.characterSpriteSheet = pygame.image.load('res/8x8CGACodePage.png').convert()
		self.characterArray = surfarray.array3d(self.characterSpriteSheet)
		
	
	def makeSentence(self, sentence):
		resultImage = pygame.Surface((len(sentence)*8, 8))
		count = 0;
		for c in sentence:
			resultImage.blit(self.getChar(c), (count*8,0), (0,0,8,8))
			count+=1
		return resultImage
		
		
	def getChar(self, char):
		charValue = ord(char)
		col = charValue % 32
		row = int(charValue / 32)
		charImage = pygame.Surface((8,8))
		
		#set the background color
		charImage.fill(self.backgroundColor)
		
		#Crop character from spritesheet
		charImage.blit(self.characterSpriteSheet, (0,0), (col*8, row*8, 8, 8))
		
		#set the font color
		charImage = self.colorReplace(charImage, (255,255,255), self.fontColor)
		
		return charImage

	def update(self):
		#print matrix to console
		#~ print(self.matrix)
		
		#draw pixels onto pygame window
		if self.previewEnabled:
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
		curved_color = self.toGamma(color)
		self.bs.set_color (0, self.softToHardPixel(x, y), *curved_color)
		self.bs.send_data(0)
		
	def toGamma(self, color):
		if self.useGamma:
			return (self.gamma[int(color[0])], self.gamma[int(color[1])], self.gamma[int(color[2])])
		return color
		
	def getPixel(self, x, y):
		return self.matrix[y][x]
		
	def drawSurface(self, surface):
		if (surface.get_width() < self.width): return
		for x in range (0, self.width):
			for y in range (0, self.height):
				color = surface.get_at((x, y))
				self.matrix[y][x] = (color.r, color.g, color.b)
				curved_color = color
				if self.useGamma:
					curved_color = (self.gamma[int(color[0])], self.gamma[int(color[1])], self.gamma[int(color[2])])
				self.bs.set_color (0, self.softToHardPixel(x, y), *curved_color)
		self.bs.send_data(0)
	
	def randomColor(self):
		return self.toGamma((randint(0,255), randint(0,255), randint(0,255)))

	#http://stackoverflow.com/questions/5891808/how-to-invert-colors-of-an-image-in-pygames
	def invertImage(self,img):
		inv = pygame.Surface(img.get_rect().size, pygame.SRCALPHA)
		inv.fill((255,255,255,255))
		inv.blit(img, (0,0), None, BLEND_RGB_SUB)
		return inv
	
	#http://stackoverflow.com/questions/15076133/pygame-edit-colours-of-an-image-makes-white-red-at-255-0-0-without-numerical
	def colorReplace(self, surface, find_color, replace_color):
		for x in range(surface.get_size()[0]):
			for y in range(surface.get_size()[1]):
				if surface.get_at([x, y]) == find_color:
					surface.set_at([x, y], replace_color)
		return surface
		

#Main
if __name__ == "__main__":
	CANOPTO = Canopto(2, 8, previewEnabled = True, useGamma = True)
	
	sentence = "Hello"
	#~ for i in range(0,255):
		#~ sentence += chr(i)
		
	sentenceSurface = CANOPTO.makeSentence(sentence)
	
	
	loopCount = 0
	fps = 10
	running = True
	sentenceBuffer = ""
	while running:
		for event in pygame.event.get():
			if event.type==QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if (event.key == K_KP_MINUS):
					fps -= 1
					if (fps <= 0): fps = 1
					print("Speed: " + fps)
				elif (event.key == K_KP_PLUS):
					fps += 1
					print("Speed: " + fps)
				else:
					sentenceBuffer += chr(event.key)
		prevTime = pygame.time.get_ticks()
		CANOPTO.drawSurface(sentenceSurface)
		
		sentenceSurface.scroll(dx=-1)
		loopCount+=1
		#If a char just passed by
		if (loopCount % 8 == 0):
			#~ CANOPTO.backgroundColor = CANOPTO.randomColor() #Uncomment to make every character have a different background color
			sentence = sentence[1:]
			sentence = sentence + sentenceBuffer
			sentenceBuffer = ""
			sentenceSurface = CANOPTO.makeSentence(sentence)
			if (len(sentence) > 0):
				print(sentence)
		
		CANOPTO.update()
		CANOPTO.clock.tick(fps)
	
	
	
	
	
