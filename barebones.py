import pygame
import button

pygame.init()
pygame.display.set_caption("barebones")
screen = pygame.display.set_mode((1280, 720),0,32)
display = pygame.Surface((600, 600))
placementGrid = pygame.Surface((500, 500))
P1Grid = pygame.Surface((500, 500))
P2Grid = pygame.Surface((500, 500))

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
battleship3_tile = pygame.image.load("images\isometric tiles/bttlship2.png").convert_alpha()
battleship4_tile = pygame.image.load("images\isometric tiles\cruiser3.png").convert_alpha()
battleshipC_tile = pygame.image.load("images\isometric tiles\cruiserC.png").convert_alpha()
battleshipX_tile = pygame.image.load("images\isometric tiles\cruiserX.png").convert_alpha()

carrier1_tile = pygame.image.load("images\isometric tiles\carrier1.png").convert_alpha()
carrier2_tile = pygame.image.load("images\isometric tiles\carrier2.png").convert_alpha()
carrier3_tile = pygame.image.load("images\isometric tiles\carrier3.png").convert_alpha()
carrier4_tile = pygame.image.load("images\isometric tiles\carrier4.png").convert_alpha()
carrierC_tile = pygame.image.load("images\isometric tiles\carrierC.png").convert_alpha()
carrierX_tile = pygame.image.load("images\isometric tiles\carrierX.png").convert_alpha()

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
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 10, 11, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99],
]

StoredBoats = [1, 1, 1, 1, 1]

def switch(screen):
    global game_screen
    game_screen = screen
    print(screen)

selected_boat = 0
cur_boat_len = 2
selected_cell = pygame.Vector2(0,0)
mov_cd = 0
rot_cd = 0
cursor_dir = 0
swap_cd = 0
bad_cell = False
stamp_cd = 0

destroyer: dict = {0: dstryr2_tile,
                    1: dstryr1_tile
                    }
submarine: dict = {0: sub3_tile,
                    1: sub2_tile,
                    2: sub1_tile
                    }
cruiser: dict = {0: cruiser3_tile,
                    1: cruiser2_tile,
                    2: cruiser1_tile
                    }
battleship: dict = {0: battleship4_tile,
                    1: battleship3_tile,
                    2: battleship2_tile,
                    3: battleship1_tile
                    }
carrier: dict = {0: carrier4_tile,
                    1: carrier2_tile,
                    2: carrier3_tile,
                    3: carrier2_tile,
                    4: carrier1_tile
                    }
boats: dict = {0: destroyer,
                1: submarine,
                2: cruiser,
                3: battleship,
                4: carrier,
                5: "none"
                }
boat_len: dict = {0: 2,
                  1: 3,
                  2: 3,
                  3: 4,
                  4: 5,
                  5: 0}

running = True
while running:

    screen.fill((0, 0, 0))
    display.fill((0, 0, 0))
    placementGrid.fill((0, 0, 0))
    P1Grid.fill((0, 0, 0))
    P2Grid.fill((0, 0, 0))

    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    if game_screen == "options":
        switch("boat placing")
        selected_boat = 0
        cur_boat_len = 2
        selected_cell = pygame.Vector2(0,0)
        mov_cd = 0

    elif game_screen == "boat placing":
        for y, row in enumerate(P1Boats):
            for x, tile in enumerate(row):
                xdil = 16
                ydil = 8
                keys = pygame.key.get_pressed()


                if keys[pygame.K_1]:
                    selected_boat = 0
                    cur_boat_len = boat_len[selected_boat]
                if keys[pygame.K_2]:
                    selected_boat = 1
                    cur_boat_len = boat_len[selected_boat]
                if keys[pygame.K_3]:
                    selected_boat = 2
                    cur_boat_len = boat_len[selected_boat]
                if keys[pygame.K_4]:
                    selected_boat = 3
                    cur_boat_len = boat_len[selected_boat]
                if keys[pygame.K_5]:
                    selected_boat = 4
                    cur_boat_len = boat_len[selected_boat]

                if mov_cd <= 0:
                    if keys[pygame.K_w] and selected_cell.y > 0:
                        selected_cell.y -= 1
                        mov_cd = 10
                    if keys[pygame.K_s] and selected_cell.y < 9:
                        selected_cell.y += 1
                        mov_cd = 10
                    if keys[pygame.K_a] and selected_cell.x > 0:
                        selected_cell.x -= 1
                        mov_cd = 10
                    if keys[pygame.K_d] and selected_cell.x < 9:
                        selected_cell.x += 1
                        mov_cd = 10
                
                if rot_cd <= 0 and keys[pygame.K_r]:
                    cursor_dir = cursor_dir*(-1) + 1
                    rot_cd = 15

                if x == selected_cell.x and y == selected_cell.y:
                    for i in range(0, cur_boat_len):
                        if cursor_dir == 0 and P1Boats[y][x+i] != 00:
                            bad_cell = True
                        if cursor_dir == 1 and P1Boats[y+i][x] != 00:
                            bad_cell = True
                else:
                    bad_cell = False
                
                funcs: dict = {00: sea_tile,
                            10: dstryr2_tile,
                            11: dstryr1_tile,
                            20: sub3_tile,
                            21: sub2_tile,
                            22: sub1_tile,
                            30: cruiser3_tile,
                            31: cruiser2_tile,
                            32: cruiser1_tile,
                            40: battleship4_tile,
                            41: battleship3_tile,
                            42: battleship2_tile,
                            43: battleship1_tile,
                            50: carrier4_tile,
                            51: carrier2_tile,
                            52: carrier3_tile,
                            53: carrier2_tile,
                            54: carrier1_tile
                            }
                tile_sprite = funcs.get(tile, "blank")
                    
                funcs: dict = {sea_tile: 00,
                            dstryr2_tile: 10,
                            dstryr1_tile: 11,
                            sub3_tile: 20,
                            sub2_tile: 21,
                            sub1_tile: 22,
                            cruiser3_tile: 30,
                            cruiser2_tile: 31,
                            cruiser1_tile: 32,
                            battleship4_tile: 40,
                            battleship3_tile: 41,
                            battleship2_tile: 42,
                            battleship1_tile: 43,
                            carrier4_tile: 50,
                            carrier2_tile: 51,
                            carrier3_tile: 52,
                            carrier2_tile: 53,
                            carrier1_tile: 54
                            }
                
                if stamp_cd <= 0 and keys[pygame.K_e]:
                    for i, line in enumerate(P1Boats):
                        for j, cell in enumerate(line):
                            for e in range(1, cur_boat_len + 1):
                                if i == selected_cell.x and j == selected_cell.y:
                                    if cursor_dir == 0 and P1Boats[j][i+e-1] != 00:
                                        bad_cell = True
                                    if cursor_dir == 1 and P1Boats[j+e-1][i] != 00:
                                        bad_cell = True
                            if bad_cell == False:
                                for e in range(1, cur_boat_len + 1):
                                    if cursor_dir == 0 and (i == selected_cell.x + e - 1) and (j == selected_cell.y):
                                        P1Boats[j][i] = funcs.get(boats.get(selected_boat).get(e - 1), 99)
                                    if cursor_dir == 1 and (i == selected_cell.x) and (j == selected_cell.y + e - 1):
                                        P1Boats[j][i] = funcs.get(boats.get(selected_boat).get(e - 1), 99)
                    if bad_cell == False:
                        StoredBoats[selected_boat] = 0
                        i = 0
                        store_clear = True
                        for boat in StoredBoats:
                            if boat == 1:
                                selected_boat = i
                                print(selected_boat)
                                print("break")
                                store_clear = False
                                break
                            i += 1
                        if store_clear == True:
                        cur_boat_len = boat_len[selected_boat]
                        stamp_cd = 30
                                    
                            

                
                if (x == selected_cell.x) and (y == selected_cell.y):
                    if (((cursor_dir == 0) and (selected_cell.x + cur_boat_len < 11)) or ((cursor_dir == 1) and (selected_cell.y + cur_boat_len < 11))) and bad_cell == False:
                        funcs: dict = {0: dstryrC_tile,
                                1: subC_tile,
                                2: cruiserC_tile,
                                3: battleshipC_tile,
                                4: carrierC_tile
                                }
                    else:
                        funcs: dict = {0: dstryrX_tile,
                                1: subX_tile,
                                2: cruiserX_tile,
                                3: battleshipX_tile,
                                4: carrierX_tile
                                }
                    tile_sprite = funcs.get(selected_boat, "blank")
                if cursor_dir == 0:
                    if (x > selected_cell.x and x < (selected_cell.x + cur_boat_len)):
                        for i in range(1, cur_boat_len):
                            if y == selected_cell.y and x == selected_cell.x + i:
                                tile_sprite = boats.get(selected_boat).get(i)
                                if tile_sprite != "blank":
                                    if x > 9 or bad_cell == True:
                                        tile_sprite.set_alpha(155)
                                    else:
                                        tile_sprite.set_alpha(255)

                else:
                    if (y > selected_cell.y and y < (selected_cell.y + cur_boat_len)):
                        for i in range(1, cur_boat_len):
                            if x == selected_cell.x and y == selected_cell.y + i:
                                tile_sprite = boats.get(selected_boat).get(i)
                                if tile_sprite != "blank":
                                    if y > 9 or bad_cell == True:
                                        tile_sprite.set_alpha(155)
                                    else:
                                        tile_sprite.set_alpha(255)
                if tile_sprite == "blank":
                    pass
                elif tile_sprite == sea_tile or cursor_dir == 0:
                    placementGrid.blit(tile_sprite, (150+x*xdil-y*xdil, 0+x*ydil+y*ydil))
                else:
                    placementGrid.blit(pygame.transform.flip(tile_sprite, True, False), (150+x*xdil-y*xdil, 0+x*ydil+y*ydil))
        
        mov_cd -= 1
        rot_cd -= 1
        swap_cd -= 1
        stamp_cd -=1

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
    screen.blit(pygame.transform.scale(placementGrid, (screen.get_width()/1.2, screen.get_width()/1.2)), (450,50))
    pygame.display.update()

pygame.quit()