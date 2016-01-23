#!/bin/python3

from Canopto import Canopto
from pygame import *
from pygame.locals import *
import time
from random import randint
from colorsys import *

# from somewhere online: http://code.activestate.com/recipes/66472/
def frange4(end,start=0,inc=0,precision=1):
    """A range function that accepts float increments."""
    import math

    if not start:
        start = end + 0.0
        end = 0.0
    else: end += 0.0

    if not inc:
        inc = 1.0
    count = int(math.ceil((start - end) / inc))

    L = [None] * count

    L[0] = end
    for i in (xrange(1,count)):
        L[i] = L[i-1] + inc
    return L

display_size = (2, 8)
cans = Canopto (display_size[0], display_size[1], False, False)

# Create image of random colors with a constant lightness
# Fade it over the previous image
# Delay
# Repeat forever

old_image = Surface(display_size)
while True:
	new_image = Surface(display_size)
	new_image.set_at((randint(0, 1), randint(0, 8)), Color(55, 55, 255))
	
	# Fade onto old image
	for alpha in range (0, 256, 4):
		intermediate_image = Surface(display_size, 0, old_image)
		new_image.set_alpha(alpha)
		intermediate_image.blit(new_image, (0, 0))
		cans.drawSurface(intermediate_image)
		
		time.sleep(0.1)
	