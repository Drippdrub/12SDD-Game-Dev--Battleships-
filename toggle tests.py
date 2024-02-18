import pygame
import customwidgets as widgets

clock = pygame.time.Clock()
wn_size = (800, 600)
pygame.init()

screen = pygame.display.set_mode(wn_size)

mode1p_img = pygame.image.load("images/button_Mode1P.png").convert_alpha()
mode2p_img = pygame.image.load("images/button_Mode2P.png").convert_alpha()
mode1p1_img = pygame.image.load("images/toggle_select1P.png").convert_alpha()
mode2p2_img = pygame.image.load("images/toggle_select2P.png").convert_alpha()

toggle_button = widgets.Toggle(400, 200, mode1p_img, mode2p_img, 3)
toggle_button2 = widgets.Toggle(400, 400, mode1p1_img, mode2p2_img, 1.5)

running = True
while running:
    screen.fill((52, 78, 91))
    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False
    toggle_button.draw(screen)
    toggle_button2.draw(screen)
    pygame.display.update()