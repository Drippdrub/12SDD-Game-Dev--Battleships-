import pygame
# import button.py custom module
import button

# pygame setup
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle Ships (Main Menu)")
clock = pygame.time.Clock()
running = True
dt = 0

# game variables
screens = ["Startup Animation", "Main Menu", "1P Options", "2P Options", "Game"]
game_screen = screens[0]
# define fonts
font = pygame.font.SysFont("arialblack", 40)

# define colours
TEXT_COL = (225, 225, 225)

# load button images
title_img = pygame.image.load("images/title.png").convert_alpha()
play_img = pygame.image.load("images/button_play.png").convert_alpha()

# create button instances
title_button = button.Button(SCREEN_WIDTH/2, 100, title_img, 7)
play_button = button.Button(SCREEN_WIDTH/2, 500, play_img, 3)

# load sounds
startup_sfx1 = pygame.mixer.Sound("sounds/SFX/Explosion1.wav")
startup_sfx1.set_volume(0.5)
startup_sfx2 = pygame.mixer.Sound("sounds\SFX\Blip1")
startup_sfx2.set_volume(0.5)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

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
            game_screen = screens[1]

        if 30 < startup_ticks < 50:
            title_button = button.Button(SCREEN_WIDTH/2, 100, title_img, (7+((50-startup_ticks)*1)))
            title_button.draw(screen)
        elif startup_ticks == 50:
            title_button = button.Button(SCREEN_WIDTH/2, 100, title_img, 7)
            title_button.draw(screen)
            pygame.mixer.Sound.play(startup_sfx1)
        elif startup_ticks > 50:
            title_button.draw(screen)

        if startup_ticks == 90:
            pygame.mixer.Sound.play(startup_sfx2)
        if startup_ticks >= 90:
            play_button.draw(screen)

        startup_ticks += 1


    elif game_screen == screens[1]:
        title_button.draw(screen)
        if play_button.draw(screen):
            game_screen = screens[2]


    elif game_screen == screens[2]:
        passqlqlqlqlql


    elif game_screen == screens[3]:
        draw_text("Press SPACE to pause", font, TEXT_COL, 160, 250)



    dt = clock.tick(60) / 1000

    pygame.display.update()

pygame.quit()