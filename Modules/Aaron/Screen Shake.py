import pygame
from itertools import repeat
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# set screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
org_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32) #parent screen
screen = org_screen.copy() #buffer screen, used to screen-shake. All children are blit to this surface, and this surface is blit to org_screen

offset = repeat((0, 0))

def shake():
    s = -1
    for _ in iter(range(0, 2)):
        for x in range(0, 20, 5):
            i = x*s*0.3
            for y in range(0, 10, 5):
                j = y*s*0.1
                yield (i, j)
        for x in range(20, 0, 5):
            i = x*s*0.3
            for y in range(10, 0, 5):
                j = y*s*0.1
                yield (i, j)
        s *= -1
    while True:
        yield (0, 0)

if __name__ == "__main__":
    img = pygame.image.load(resource_path("images\ooga_booga.png")).convert_alpha()
    running = True
    cd = 0
    while running:
        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked X to close your window
            if event.type == pygame.QUIT:
                running = False
        
        if cd >= 500:
            offset = shake()
            cd = 0
        cd += 1

        screen.blit(pygame.transform.scale(img, (300, 300)), (640, 320))
        try:
            org_screen.blit(screen, next(offset))
        except:
            org_screen.blit(screen, (0, 0))

        pygame.display.update()