#!/bin/python3

from Canopto import Canopto
import pygame
from pygame import *
from pygame.locals import *
import time
from random import randint
from colorsys import *
import sys
import numpy
import math


display_size = (4, 8)
cans = Canopto (display_size[0], display_size[1], True, True)

# Plays Conway's Game of Life over the display, fading in each new frame over the last
# Still life and cycle detection is provided by storing every frame of every simulation,
# and comparing each new frame to all the previous. If there are any matches, the
# game ends after a set number more frames are rendered (10-ish).

# Graphical plan: fade in each new frame on top of the last, showing the last dimly
# behind the current. When about to reset, pulse the background red or yellow. 
# Otherwise keep the background black.
# The foreground color will change with each simulation, always bright.

def randomize_frame (input_frame):
	input_frame = [[randint(0, 1)
		for x in range (display_size[0])] 
		for y in range (display_size[1])]
	return input_frame
	
def calculate_frame (last_frame):
	#print ("CALCULATE_FRAME")
	#print ("Input:")
	#print (last_frame)

	# Make an empty new frame
	width = len(last_frame[0])
	height = len(last_frame)
	#new_frame = [[0] * width] * height
	new_frame = [x[:] for x in last_frame]
	
	# Iterate over each cell in last_frame
	for x in range (width):
		for y in range (height):
			#print ("Cell ", (x, y))
		
			# For each cell, sum up the number of neighbors in the adjacent cells
			neighbors = 0
			for (rel_x, rel_y) in [
				(x-1, y-1), (x, y-1), (x+1, y-1), 
				(x-1, y), (x+1, y), (x-1, y+1), 
				(x, y+1), (x+1, y+1)]:
				# Neigbors only possible in-bounds
				if (0 <= rel_x < width) and (0 <= rel_y < height):
					#print ("      In cell ", (rel_x, rel_y), " last_frame is ", (last_frame[rel_y][rel_x]))
					if (last_frame[rel_y][rel_x] == 1):
						neighbors += 1
			#print ("Neighbors ", neighbors)					
			
			# Change new cell based on past cell state and number of neighbors
			new_frame[y][x] = last_frame[y][x]
			if (last_frame[y][x] == 1):
				if neighbors < 2:
					new_frame[y][x] = 0
				elif (neighbors == 2) or (neighbors == 3):
					new_frame[y][x] = 1
				elif neighbors > 3:
					new_frame[y][x] = 0
			else:
				if neighbors == 3:
					new_frame[y][x] = 1
			#print ("Now new frame at ", (x, y)," is ", new_frame[y][x])
	
	#print ("Resulting frame: ")
	#print (new_frame)
	return new_frame

def check_for_cycles (history, new_frame):
	def frames_equal (frame1, frame2):
		for x in range(len(frame1[0])):
			for y in range(len(frame1)):
				if (frame1[y][x] != frame2[y][x]):
					return False
		return True

	# Check new frame against history of frames for duplicates
	for frame in history:
		if (frames_equal(frame, new_frame)):
			return True
	return False

def frame_to_surface (frame, fg, alpha=255):
	"""Converts a 2D frame of values from 0 to 1 to a surface with fg 
	foreground color and bg background color"""
	surface = Surface ((len(frame[0]), len(frame)))
	for x in range (len(frame[0])):
		for y in range (len(frame)):
			if (frame[y][x] != 0):
				surface.set_at((x, y), fg)
	surface.set_alpha(alpha)
	return surface
	
def darken (color, percent):
	dark_color = Color (round(color.r * percent), 
						round(color.g * percent), 
						round(color.b * percent), color.a)
	return dark_color

# Play simulations forever
while True:
	# Create 2D array for last frame, and a random starting frame
	last_frame = [[0] * display_size[0]] * display_size[1]
	curr_frame = randomize_frame(last_frame)
	# Create empty 3D array for frame history
	history = []
	
	# Choose look of this simulation
	cell_color = Color (0, 0, 0, 255)
	cell_color_hue = randint(0, 359)
	cell_color.hsla = (cell_color_hue, 100, 50, 100)
	
	# Run frames of each simulation until they are stuck in a cycle
	# or still life
	remaining_frames = None
	while (remaining_frames == None) or (remaining_frames > 0):
		# TODO Render transition to new frame
		cell_color_hue = (cell_color_hue + 3) % 360
		cell_color.hsla = (cell_color_hue, 100, 50, 100)
		surface = Surface(display_size)
		surface.fill(Color(0, 0, 0))
		surface.blit(frame_to_surface(curr_frame, cell_color), (0, 0))
		cans.drawSurface(surface)
		cans.update()
		for event in pygame.event.get():
			if event.type==QUIT:
				sys.exit(0)
		time.sleep(0.1)
		
		# Log previous frame into last frame and the history
		history.append(curr_frame)
		last_frame = curr_frame
		
		# Calculate current frame
		curr_frame = calculate_frame(last_frame)
		# Check for still lifes and cycles
		if remaining_frames == None:
			if check_for_cycles(history, curr_frame):
				# Start a frames countdown to next simulation
				remaining_frames = 7
		
		# Update remaining frames
		if remaining_frames != None:
			remaining_frames -= 1

# while True:
	# # Make an image 1000 pixels wide
	# lines = Surface((1000, display_size[1]+2))
	# lines.fill(Color(0, 0, 92, 255))
	
	# # Draw lines
	# # Come up with sets of points. Alternate between high and low lines. Allow random space between each, and generate up to the end of the surface
	
	# # Simple algorithm: generate one line. 
	# margin = 5
	# currX = margin
	# points = [(margin, randint(0, lines.get_height()-1))]
	# while currX < lines.get_width() - margin:
		# currX = randint(currX+7, currX+30)
		# currX = min(lines.get_width()-margin, currX)
		# points.append ((currX, randint(1, lines.get_height()-2)))
		
	# # Draw line from points
	# #line_color = Color(54, 255, 54, 255)
	# line_color = Color(255, 128, 0, 255)
	# pygame.draw.aalines(lines, line_color, False, points)
	
	# # Scroll image across canopto
	# for x in range (0, lines.get_width()-(display_size[0]-1)):
		# frame = Surface (display_size)
		# frame.blit (lines, (-x, -1))
		# cans.drawSurface(frame)
		
		# cans.update()
		# for event in pygame.event.get():
			# if event.type==QUIT:
				# sys.exit(0)
		# time.sleep(0.03)