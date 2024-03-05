import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
pygame.display.set_caption("barebones")
org_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)
screen = org_screen.copy()
hud = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA, 32).convert_alpha()
leftRender = pygame.Surface((320, 320)).convert_alpha()
leftOverlay = pygame.Surface((320, 320)).convert_alpha()
rightRender = pygame.Surface((320, 320)).convert_alpha()
rightOverlay = pygame.Surface((320, 320)).convert_alpha()
placementSurface = pygame.Surface((400, 400)).convert_alpha()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))