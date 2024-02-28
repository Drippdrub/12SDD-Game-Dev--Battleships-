#!/usr/bin/python
import os
import pygame, sys
from pygame.locals import *

# set window size
width = 640
height = 100

# initilaise pygame
pygame.init()
windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
redColor = pygame.Color(255,0,0)
blackColor = pygame.Color(0,0,0)

#starting position
x = 100
pygame.draw.rect(windowSurfaceObj,redColor,Rect(x,5,10,90))
pygame.display.update(pygame.Rect(0,0,width,height))

s = 0
while s == 0:
    button = pygame.mouse.get_pressed()
    if button[0] != 0:
       pos = pygame.mouse.get_pos()
       x = pos[0]
       y = pos[1]
       a = x - 5
       if a < 0:
          a = 0
       pygame.draw.rect(windowSurfaceObj,blackColor,Rect(0,0,width,height))
       #pygame.display.update(pygame.Rect(0,0,width,height))
       pygame.draw.rect(windowSurfaceObj,redColor,Rect(a,5,10,90))
       pygame.display.update(pygame.Rect(0,0,width,height))


   # check for ESC key pressed, or pygame window closed, to quit
    for event in pygame.event.get():
       if event.type == QUIT:
          pygame.quit()
          sys.exit()
       elif event.type == KEYDOWN:
          if event.key == K_ESCAPE:
             pygame.quit()
             sys.exit()