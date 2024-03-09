import pygame
import sys
import os
import random
from tkinter import *
from tkinter import messagebox
import copy
import math
from itertools import repeat

import customwidgets as widgets

# set screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# used for pyinstaller compatability
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# initialise pygame
pygame.init()

# set surfaces
org_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32) #parent screen
screen = org_screen.copy() #buffer screen, used to screen-shake. All children are blit to this surface, and this surface is blit to org_screen
hud = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA, 32).convert_alpha() #overlay surface. blit last, so all object in this layer are always on top
leftRender = pygame.Surface((320, 320)).convert_alpha() #renders leftside grid in game
leftOverlay = pygame.Surface((320, 320)).convert_alpha() #renders cursor, bombs and animations on top of leftside grid in game
rightRender = pygame.Surface((320, 320)).convert_alpha() #renders rightside grid in game
rightOverlay = pygame.Surface((320, 320)).convert_alpha() #renders bombs and animations on top of rightside grid in game
placementSurface = pygame.Surface((400, 400)).convert_alpha() #renders grid for boat placement

# font imports
font1 = pygame.font.Font(resource_path("fonts\CompassPro.ttf"), 72)
font2 = pygame.font.Font(resource_path("fonts\Crang.ttf"), 84)
font3 = pygame.font.Font(resource_path("fonts\CompassPro.ttf"), 36)
font4 = pygame.font.Font(resource_path("fonts\CompassPro.ttf"), 28)
font5 = pygame.font.Font(resource_path("fonts\CompassPro.ttf"), 18)

# button press sound 
blip = pygame.mixer.Sound(resource_path("sounds\SFX\Blip2.wav"))
blip.set_volume(0.75)

playButton_img = pygame.image.load(resource_path("images/button_play.png")).convert_alpha()
playButton_hover = pygame.image.load(resource_path("images/button_play_hover.png")).convert_alpha()
backButton_img = pygame.image.load(resource_path("images/button_back.png")).convert_alpha()
backButton_hover = pygame.image.load(resource_path("images/button_back_hover.png")).convert_alpha()
select1P_img = pygame.image.load(resource_path("images/toggle_select1P.png")).convert_alpha()
select2P_img = pygame.image.load(resource_path("images/toggle_select2P.png")).convert_alpha()
selectDiffEasy_img = pygame.image.load(resource_path("images/toggle_diffEasy.png")).convert_alpha()
selectDiffHard_img = pygame.image.load(resource_path("images/toggle_diffHard.png")).convert_alpha()


# player card assets
player1Board_img = pygame.image.load(resource_path("images\Player1 Board.png")).convert_alpha()
player2Board_img = pygame.image.load(resource_path("images\Player2 Board.png")).convert_alpha()
ai_easy_Board_img = pygame.image.load(resource_path("images\AI Easy Board.png")).convert_alpha()
ai_hard_Board_img = pygame.image.load(resource_path("images\AI Hard Board.png")).convert_alpha()

# empty boxes
middle_Board_img = pygame.image.load(resource_path("images\Middle Board.png")).convert_alpha()

timeoff_img = pygame.image.load(resource_path("images/time_off.png")).convert_alpha()
time60s_img = pygame.image.load(resource_path("images/time_60.png")).convert_alpha()
time90s_img = pygame.image.load(resource_path("images/time_90.png")).convert_alpha()
time3m_img = pygame.image.load(resource_path("images/time_3m.png")).convert_alpha()
time5m_img = pygame.image.load(resource_path("images/time_5m.png")).convert_alpha()
time10m_img = pygame.image.load(resource_path("images/time_10m.png")).convert_alpha()

help_icon = pygame.image.load(resource_path("images/help.png")).convert_alpha()

# game options widgets
space = 75
timeOff = widgets.Button(640-space, 260, timeoff_img, 1.3)
time60s = widgets.Button(640, 260, time60s_img, 1.3)
time90s = widgets.Button(640+space, 260, time90s_img, 1.3)
time3m = widgets.Button(640-space, 300, time3m_img, 1.3)
time5m= widgets.Button(640, 300, time5m_img, 1.3)
time10m = widgets.Button(640+space, 300, time10m_img, 1.3)
helpTime = widgets.Image(640+space+50, 260, help_icon, 0.75, "Overall time each player gets in a game.")

selectPlayer = widgets.Toggle(640, 375, select1P_img, select2P_img, 1.2)
selectDiff = widgets.Toggle(640, 475, selectDiffEasy_img, selectDiffHard_img, 0.7)
gameOptionsProceed = widgets.Button(640, 565, playButton_img, 2.75, playButton_hover)
backButton2 = widgets.Button(640, 630, backButton_img, 1.3, backButton_hover)

player1Board = widgets.Image(200, 360, player1Board_img, 1)
player2Board = widgets.Image(1080, 360, player2Board_img, 1)
aiEasyBoard = widgets.Image(1080, 360, ai_easy_Board_img, 1)
aiHardBoard = widgets.Image(1080, 360, ai_hard_Board_img, 1)
middleBoard = widgets.Image(640, 360, middle_Board_img, 1)

def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    hud.blit(img, (x, y))

# function to switch game screen, also prints for debug
def switch(screen):
    global game_screen
    game_screen = screen
    print(screen)

game_screen = "game options"
selectedPlayerMode = 0
time_enabled = False
time_set = 0

running = True
while running:
    screen.fill((110, 110, 110))
    hud.fill((0, 0, 0, 0))

    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False
    
    if game_screen == "game options":
        middleBoard.draw(hud)

        if selectedPlayerMode == 0:
            selectedDiff = selectDiff.draw(hud, output=0)
            if selectedDiff == True:
                difficulty = "Hard"
                aiHardBoard.draw(hud)
            else:
                difficulty = "Easy"
                aiEasyBoard.draw(hud)
        else:
            player2Board.draw(hud)
        player1Board.draw(hud)

        draw_text("Game Options", font1, (0, 0, 0), (1280-font1.size("Game Options")[0])/2, 100)
        draw_text("Timed Game", font3, (0, 0, 0), (1280-font3.size("Timed Game")[0])/2, 200)
        if time_enabled == False:
            timeOff.draw(hud, 255)
            if time60s.draw(hud, 100):
                time_enabled = True
                time_set = 60
                pygame.mixer.Sound.play(blip)
            if time90s.draw(hud, 100):
                time_enabled = True
                time_set = 90
                pygame.mixer.Sound.play(blip)
            if time3m.draw(hud, 100):
                time_enabled = True
                time_set = 180
                pygame.mixer.Sound.play(blip)
            if time5m.draw(hud, 100):
                time_enabled = True
                time_set = 300
                pygame.mixer.Sound.play(blip)
            if time10m.draw(hud, 100):
                time_enabled = True
                time_set = 600
                pygame.mixer.Sound.play(blip)
        else:
            if timeOff.draw(hud, 100):
                time_enabled = False
                time_set = 0
                pygame.mixer.Sound.play(blip)
            times = [60, 90, 180, 300, 600]
            timeBtns = [time60s, time90s, time3m, time5m, time10m]
            for time in times:
                if time_set == time:
                    timeBtns[times.index(time)].draw(hud, 255)
                else:
                    if timeBtns[times.index(time)].draw(hud, 100):
                        time_set = time
                        pygame.mixer.Sound.play(blip)
        
        helpTime.focusCheck(pygame.mouse.get_pos(), False)
        helpTime.draw(hud)
        helpTime.showTip(hud)
        selectedPlayerMode = selectPlayer.draw(hud, output=0)
        
        if gameOptionsProceed.draw(hud):
            winner = "undecided"
            pygame.mixer.Sound.play(blip)
            switch("page router")
        if backButton2.draw(hud):
            pygame.mixer.Sound.play(blip)
            switch("main")
    
    screen.blit(hud, (0, 0))
    org_screen.blit(screen, (0, 0))
    pygame.display.update()