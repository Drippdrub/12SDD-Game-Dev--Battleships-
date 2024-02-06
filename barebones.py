import pygame
import button

pygame.init()
pygame.display.set_caption("barebones")
screen = pygame.display.set_mode((720, 720),0,32)
display = pygame.Surface((300, 300))

clock = pygame.time.Clock()

iso_test = pygame.image.load("images\iso_test.png").convert()
iso_test.set_colorkey((0, 0, 0))
ship_tile = pygame.image.load("images\isometric tiles\ship unit.png").convert()
ship_tile.set_colorkey((0, 0, 0))
sea_tile = pygame.image.load("images\isometric tiles\sea unit.png").convert()
sea_tile.set_colorkey((0, 0, 0))

dstryr1_tile = pygame.image.load("images\isometric tiles\destroyer1.png").convert_alpha()
dstryr2_tile = pygame.image.load("images\isometric tiles\destroyer2.png").convert_alpha()
dstryrX_tile = pygame.image.load("images\isometric tiles\destroyerX.png").convert_alpha()
dstryrC_tile = pygame.image.load("images\isometric tiles\destroyerC.png").convert_alpha()

sub1_tile = pygame.image.load("images\isometric tiles\sub1.png").convert_alpha()
sub2_tile = pygame.image.load("images\isometric tiles\sub2.png").convert_alpha()
sub3_tile = pygame.image.load("images\isometric tiles\sub3.png").convert_alpha()
subX_tile = pygame.image.load("images\isometric tiles\subX.png").convert_alpha()
subC_tile = pygame.image.load("images\isometric tiles\subC.png").convert_alpha()

cruiser1_tile = pygame.image.load("images\isometric tiles\cruiser1.png").convert_alpha()
cruiser2_tile = pygame.image.load("images\isometric tiles\cruiser2.png").convert_alpha()
cruiser3_tile = pygame.image.load("images\isometric tiles\cruiser3.png").convert_alpha()
cruiserX_tile = pygame.image.load("images\isometric tiles\cruiserX.png").convert_alpha()
cruiserC_tile = pygame.image.load("images\isometric tiles\cruiserC.png").convert_alpha()

battleship1_tile = pygame.image.load("images\isometric tiles/bttlship1.png").convert_alpha()
battleship2_tile = pygame.image.load("images\isometric tiles/bttlship2.png").convert_alpha()
battleship3_tile = pygame.image.load("images\isometric tiles\cruiser3.png").convert_alpha()
battleshipC_tile = pygame.image.load("images\isometric tiles\cruiserC.png").convert_alpha()

carrier1_tile = pygame.image.load("images\isometric tiles\carrier1.png").convert_alpha()
carrier2_tile = pygame.image.load("images\isometric tiles\carrier2.png").convert_alpha()
carrier3_tile = pygame.image.load("images\isometric tiles\carrier3.png").convert_alpha()
carrier4_tile = pygame.image.load("images\isometric tiles\carrier4.png").convert_alpha()
carrierC_tile = pygame.image.load("images\isometric tiles\carrierC.png").convert_alpha()

game_screen = "boat placing"

TestArr = [
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 10, 11, 00, 00, 00, 00, 00, 00, 00],
    [00, 20, 21, 22, 00, 00, 00, 00, 00, 00],
    [00, 30, 31, 32, 00, 00, 00, 00, 00, 00],
    [00, 40, 41, 42, 43, 00, 00, 00, 00, 00],
    [00, 50, 51, 52, 53, 54, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00]
]

P1Boats = [
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00]
]

StoredBoats = [1, 1, 1, 1, 1]

def switch(screen):
    global game_screen
    game_screen = screen
    print(screen)

selected_cell = pygame.Vector2(0,0)
mov_cd = 0
rot_cd = 0
cursor_dir = 0

running = True
while running:

    screen.fill((0, 0, 0))
    display.fill((0, 0, 0))

    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    if game_screen == "options":
        switch("boat placing")
        selected_boat = "dstryr"
        selected_cell = pygame.Vector2(0,0)
        mov_cd = 0

    elif game_screen == "boat placing":
        for y, row in enumerate(P1Boats):
            for x, tile in enumerate(row):
                xdil = 16
                ydil = 8
                keys = pygame.key.get_pressed()

                if mov_cd <= 0:
                    if keys[pygame.K_w] and selected_cell.y > 0:
                        selected_cell.y -= 1
                        mov_cd = 1500
                    if keys[pygame.K_s] and selected_cell.y < 9:
                        selected_cell.y += 1
                        mov_cd = 1500
                    if keys[pygame.K_a] and selected_cell.x > 0:
                        selected_cell.x -= 1
                        mov_cd = 1500
                    if keys[pygame.K_d] and selected_cell.x < 9:
                        selected_cell.x += 1
                        mov_cd = 1500
                
                if rot_cd <= 0 and keys[pygame.K_r]:
                    cursor_dir = cursor_dir*(-1) + 1
                    rot_cd = 1500

                mov_cd -= 1
                rot_cd -= 1

                # pygame.draw.rect(display, (255, 255, 255), pygame.Rect(x*10, y*10, 10, 10), 1)
                funcs: dict = {00: sea_tile}
                tile_sprite = funcs.get(tile, sea_tile)
                if (x == selected_cell.x) and (y == selected_cell.y):
                    tile_sprite = dstryrC_tile
                if tile_sprite == sea_tile or cursor_dir == 0:
                    display.blit(tile_sprite, (150+x*xdil-y*xdil, 0+x*ydil+y*ydil))
                else:
                    display.blit(pygame.transform.flip(tile_sprite, True, False), (150+x*xdil-y*xdil, 0+x*ydil+y*ydil))

        # switch("game")
        
    elif game_screen == "game":
        for y, row in enumerate(P1Boats):
            for x, tile in enumerate(row):
                xdil = 16
                ydil = 8
                # pygame.draw.rect(display, (255, 255, 255), pygame.Rect(x*10, y*10, 10, 10), 1)
                funcs: dict = {00: sea_tile,
                            10: dstryr2_tile,
                            11: dstryr1_tile,
                            20: sub3_tile,
                            21: sub2_tile,
                            22: sub1_tile,
                            30: cruiser3_tile,
                            31: cruiser2_tile,
                            32: cruiser1_tile,
                            40: cruiser3_tile,
                            41: cruiser2_tile,
                            42: battleship2_tile,
                            43: battleship1_tile,
                            50: carrier4_tile,
                            51: carrier2_tile,
                            52: carrier3_tile,
                            53: carrier2_tile,
                            54: carrier1_tile
                            }
                tile_sprite = funcs.get(tile, sea_tile)
                display.blit(tile_sprite, (150+x*xdil-y*xdil, 0+x*ydil+y*ydil))
    
    dt = clock.tick(60) / 1000
    screen.blit(pygame.transform.scale(display, screen.get_size()), (0,0))
    pygame.display.update()

pygame.quit()