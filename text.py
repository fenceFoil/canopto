#!/bin/python3

from Canopto import Canopto
import pygame
from pygame import *
from pygame.locals import *
import time
from colorsys import *
import sys
import json
import datetime

# scroll text across canopto. blocks. fg & bg are colors
def scrollText (canopto, text, fg = (0xFF, 0x33, 0xFF), bg = (0x00, 0x00, 0x00, 0x00), font = "16bfZX", yOffset = 2):
	#TinyUnicode 16, offset 5
	#Habbo 12, offset 0
	#16bfZX 16, offset 2
	#surface = pygame.font.SysFont("16bfZX", 16).render(text, False, fg, bg)
	surface = pygame.font.Font(font+".ttf", 16).render(text, False, fg, bg)
	scrollSurface(canopto, surface, speed = 1.2, yOffset = 2)

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

# Main
if __name__ == "__main__":
	c = Canopto(8, 8, previewEnabled=True, useGamma=True)
	#scrollText (c, "HI GEESE yeah you're pretty cool xDDDD :) Hi!");
	scrollText (c, "    trying small letters    ");
	
# if __name__ == "__main__":
	# display = Canopto (8, 8, previewEnabled=True, useGamma=True)

	# CONFIG_PATH = 'config.json'
	# # API KEYS FOUND HERE: https://www.twilio.com/user/account  (NOT  under DEV TOOLS > API KEYS)
	# # Read API keys for Twilio from json config file (outside of git repository)
	# # Or use environment variables as https://github.com/twilio/twilio-python suggests
	# with open(CONFIG_PATH) as json_config:
		# config = json.load(json_config)
		# ACCOUNT_SID = config['twilio']['account_sid']
		# AUTH_TOKEN = config['twilio']['auth_token']
		# print("Successfuly read api information from config")

	# client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

	# processedMessages = []
	# processedIDs = []

	# startTime = datetime.datetime.now() + datetime.timedelta(hours=4)

	# while (True): #display.tracker.running):
		# #if tracker.frameCounter == 10:
			# #tracker.resetToMotion = True
			# #print "reset to motion"
		# print ("hihi")
		# #Because of a conflict between timezones used to represent dates cannot limit by day since messages sent after
		# #~10pm will, according to server, be sent tomorrow thereby not having them show up as new messages if limited by today
		# #date_sent=datetime.datetime.today()
		# messages = client.messages.list()
		# print ("hi")
		# for message in messages:
			# if (message.direction == "inbound"):
				# #New message from now onward that hasn't already been processed
				# if message.sid not in processedIDs and message.date_created > startTime:
					# scrollText(display, "   " + message.body + "   ")
						
					# processedIDs.append(message.sid)
						
		# time.sleep(1)

	# #Close down the main loops of the threads
	# #tracker.running = False
	# display.clear()
	# display.running = False
