import pygame
# import button.py custom module
import customwidgets as widgets

# pygame setup
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# screen = org_screen.copy()
# screen_rect = screen.get_rect()
pygame.display.set_caption("Battle Ships (Main Menu)")
clock = pygame.time.Clock()
running = True
dt = 0

# game variables
global screens
screens = ["Startup Animation", "Main Menu", "1 Player Options", "2 Player Options", "Game"]
global game_screen
game_screen = screens[0]
# define fonts
font = pygame.font.SysFont("arialblack", 40)

# define colours
TEXT_COL = (225, 225, 225)

# load images
title_img = pygame.image.load("images/title.png").convert_alpha()
play_img = pygame.image.load("images/button_play.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
mode1p_img = pygame.image.load("images/button_Mode1P.png").convert_alpha()
mode2p_img = pygame.image.load("images/button_Mode2P.png").convert_alpha()

# create image/button instances
title_button = widgets.Button(SCREEN_WIDTH/2, 100, title_img, 7)
play_button = widgets.Button(SCREEN_WIDTH/2, 300, play_img, 3)
options_button = widgets.Button(SCREEN_WIDTH/2, 400, options_img, 3)
mode1p_button = widgets.Button(SCREEN_WIDTH/2, 360, mode1p_img, 3)
mode2p_button = widgets.Button(SCREEN_WIDTH/2, 360, mode2p_img, 3)

# load sounds
startup_sfx1 = pygame.mixer.Sound("sounds/SFX/Explosion1.wav")
startup_sfx1.set_volume(0.5)
startup_sfx2 = pygame.mixer.Sound("sounds\SFX\Blip1.wav")
startup_sfx2.set_volume(0.5)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def switch(screen):
    global game_screen
    game_screen = screens[screen]
    print(screens[screen])

startup_ticks = 0

while running:
    # poll for events
    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    screen.fill((52, 78, 91))

    if game_screen == screens[0]:
        
        if startup_ticks > 170:
            switch(1)

        if 30 < startup_ticks < 50:
            title_button = widgets.Button(SCREEN_WIDTH/2, 100, title_img, (7+((50-startup_ticks)*1)))
            title_button.draw(screen)
        elif startup_ticks == 50:
            title_button = widgets.Button(SCREEN_WIDTH/2, 100, title_img, 7)
            title_button.draw(screen)
            pygame.mixer.Sound.play(startup_sfx1)
        elif startup_ticks > 50:
            title_button.draw(screen)

        if startup_ticks == 90:
            pygame.mixer.Sound.play(startup_sfx2)
        if startup_ticks >= 90:
            play_button.draw(screen)
        
        if startup_ticks == 130:
            pygame.mixer.Sound.play(startup_sfx2)
        if startup_ticks >= 130:
            options_button.draw(screen)

        startup_ticks += 1


    elif game_screen == screens[1]:
        title_button.draw(screen)
        if play_button.draw(screen):
            switch(2)
        if options_button.draw(screen):
            pass


    elif game_screen == screens[2]:
        if mode1p_button.draw(screen):
            switch(3)
            pygame.display.update()
            pygame.time.wait(100)



    elif game_screen == screens[3]:
        if mode2p_button.draw(screen):
            switch(2)
            pygame.display.update()
            pygame.time.wait(100)




    dt = clock.tick(60) / 1000

    pygame.display.update()

pygame.quit()