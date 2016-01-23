#!/usr/bin/python
# M.E.Farmer 2013
# demo for tween library
# showing integration with PyGame
# moves text from random points using various tweens
# changes from random color to random color using the same tween
# Mouse click rotates through tweens and ESC closes demo
import sys
import pygame
import random
import tween


# higher number equal slower transitions
# stall/fps = seconds per transition
stall=offset = 60
FPS = 60
BACKGROUND_COLOR  = (0,0,0)
size = width, height = (800,600)
text_pos = (0,0)
text_color = (0,128,0)

tweens = [
          (tween.easeLinear,"easeLinear"),
          (tween.easeInQuad,"easeInQuad"),
          (tween.easeInOutQuad,"easeInOutQuad"),
          (tween.easeOutQuad,"easeOutQuad"),
          (tween.easeInCubic,"easeInCubic"),
          (tween.easeInOutCubic,"easeInOutCubic"),
          (tween.easeOutCubic,"easeOutCubic"),
          (tween.easeInQuartic,"easeInQuartic"),
          (tween.easeInOutQuartic,"easeInOutQuartic"),
          (tween.easeOutQuartic,"easeOutQuartic"),
          (tween.easeInQuintic,"easeInQuintic"),
          (tween.easeInOutQuintic,"easeInOutQuintic"),
          (tween.easeOutQuintic,"easeOutQuintic"),
          (tween.easeInSine,"easeInSine"),
          (tween.easeInOutSine,"easeInOutSine"),
          (tween.easeOutSine,"easeOutSine"),
          (tween.easeInExpo,"easeInExpo"),
          (tween.easeInOutExpo,"easeInOutExpo"),
          (tween.easeOutExpo,"easeOutExpo"),
          (tween.easeInCirc,"easeInCirc"),
          (tween.easeInOutCirc,"easeInOutCirc"),
          (tween.easeOutCirc,"easeOutCirc"),
          (tween.easeInElasticBig,"easeInElasticBig"),
          (tween.easeOutElasticBig,"easeOutElasticBig"),
          (tween.easeInElasticSmall,"easeInElasticSmall"),
          (tween.easeOutElasticSmall,"easeOutElasticSmall"),
          (tween.easeLoop,"easeLoop"),
          (tween.easeInchWorm,"easeInchWorm"),
          (tween.customTween(
           "b+c*(26.65*tc*ts + -91.5925*ts*ts + 115.285*tc + -62.89*ts + 13.5475*t)"),
           "customTween")
          ]
# setup the intial tween
tween_index = 0
ease_func,text_displayed = tweens[tween_index]

pygame.init()
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
FPSTICKER = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms",65)
text = font.render(text_displayed, True, text_color)

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if tween_index == len(tweens)-1:
                tween_index=0
            else:
                tween_index+=1
            ease_func,text_displayed = tweens[tween_index]
 
            # set our stall counter to change the tween on next check
            stall = offset
        elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                           and event.key == pygame.K_ESCAPE):
            sys.exit()
    screen.fill(BACKGROUND_COLOR)
    # the pygame clock runs faster than we want to update
    # our tweens so we just stall for a few cycles then
    # update and reset our counter 
    stall+=1
    if stall >= offset:
        stall=0
        old_pos = text_pos
        text_pos = (random.randint(1,width),random.randint(1,height))
        # set a new tween function for the coordinates
        xy_out = tween.xyTween(ease_func,old_pos,text_pos,offset,False,True)
        ##x_out = tween.tween(tween.easeLoop,old_pos[0],text_pos[0],offset,False,True)
        ##y_out = tween.tween(tween.easeInElasticSmall,old_pos[1],text_pos[1],offset,False,True)
        old_color = text_color
        text_color = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
        # set a new tween function for the text colors
        color_out  = tween.colorTween(ease_func,old_color,text_color,offset,False,True)
    # every frame we just call .next() and the tween does the work
    text = font.render(text_displayed, True, (color_out.next()))
    screen.blit(text, xy_out.next())
    ##screen.blit(text, (x_out.next(),y_out.next()))
    pygame.display.flip()
    FPSTICKER.tick(FPS)
    
