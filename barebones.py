import pygame
import button

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
pygame.display.set_caption("barebones")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)
hud = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA, 32)
hud = hud.convert_alpha()
display = pygame.Surface((600, 600))
placementGrid = pygame.Surface((500, 500))
P1Grid = pygame.Surface((500, 500))
P2Grid = pygame.Surface((500, 500))

clock = pygame.time.Clock()

denyClick_sfx1 = pygame.mixer.Sound("sounds/SFX/DenyClick.wav")
denyClick_sfx1.set_volume(0.75)

confirmFleet_img = pygame.image.load("images/button_confirmfleet.png").convert_alpha()
confirmFleet_hover = pygame.image.load("images/button_confirmfleet_hover.png").convert_alpha()

iso_test = pygame.image.load("images\iso_test.png").convert_alpha()
ship_tile = pygame.image.load("images\isometric tiles\ship unit.png").convert_alpha()

lbl_destroyer_stored = pygame.image.load("images\Placement Labels\DestroyerStored.png").convert_alpha()
lbl_destroyer_placed = pygame.image.load("images\Placement Labels\DestroyerPlaced.png").convert_alpha()
lbl_sub_stored = pygame.image.load("images\Placement Labels\SubmarineStored.png").convert_alpha()
lbl_sub_placed = pygame.image.load("images\Placement Labels\SubmarinePlaced.png").convert_alpha()
lbl_cruiser_stored = pygame.image.load("images\Placement Labels\CruiserStored.png").convert_alpha()
lbl_cruiser_placed = pygame.image.load("images\Placement Labels\CruiserPlaced.png").convert_alpha()
lbl_battleship_stored = pygame.image.load("images\Placement Labels\BattleshipStored.png").convert_alpha()
lbl_battleship_placed = pygame.image.load("images\Placement Labels\BattleshipPlaced.png").convert_alpha()
lbl_carrier_stored = pygame.image.load("images\Placement Labels\CarrierStored.png").convert_alpha()
lbl_carrier_placed = pygame.image.load("images\Placement Labels\CarrierPlaced.png").convert_alpha()

# import sea assets
sea_anim_cd = 0
cur_sea = 0
d_sea_tile = pygame.image.load("images\isometric tiles\sea unit.png").convert_alpha()
sea_tile = pygame.image.load("images\isometric tiles\sea unit.png").convert_alpha()
sea_tile2 = pygame.image.load("images\isometric tiles\sea unit2.png").convert_alpha()
sea_tile3 = pygame.image.load("images\isometric tiles\sea unit3.png").convert_alpha()

# import grid cell labels
tile_A = pygame.image.load("images\isometric tiles\Grid Labels\Acell.png").convert_alpha()
tile_B = pygame.image.load("images\isometric tiles\Grid Labels\Bcell.png").convert_alpha()
tile_C = pygame.image.load("images\isometric tiles\Grid Labels\Ccell.png").convert_alpha()
tile_D = pygame.image.load("images\isometric tiles\Grid Labels\Dcell.png").convert_alpha()
tile_E = pygame.image.load("images\isometric tiles\Grid Labels\Ecell.png").convert_alpha()
tile_F = pygame.image.load("images\isometric tiles\Grid Labels\Fcell.png").convert_alpha()
tile_G = pygame.image.load("images\isometric tiles\Grid Labels\Gcell.png").convert_alpha()
tile_H = pygame.image.load("images\isometric tiles\Grid Labels\Hcell.png").convert_alpha()
tile_I = pygame.image.load("images\isometric tiles\Grid Labels\Icell.png").convert_alpha()
tile_J = pygame.image.load("images\isometric tiles\Grid Labels\Jcell.png").convert_alpha()
tile_1 = pygame.image.load("images\isometric tiles\Grid Labels\Acell.png").convert_alpha()
tile_2 = pygame.image.load("images\isometric tiles\Grid Labels\Acell.png").convert_alpha()
tile_3 = pygame.image.load("images\isometric tiles\Grid Labels\Acell.png").convert_alpha()
tile_4 = pygame.image.load("images\isometric tiles\Grid Labels\Acell.png").convert_alpha()
tile_5 = pygame.image.load("images\isometric tiles\Grid Labels\Acell.png").convert_alpha()
tile_6 = pygame.image.load("images\isometric tiles\Grid Labels\Acell.png").convert_alpha()
tile_7 = pygame.image.load("images\isometric tiles\Grid Labels\Acell.png").convert_alpha()
tile_8 = pygame.image.load("images\isometric tiles\Grid Labels\Acell.png").convert_alpha()
tile_9 = pygame.image.load("images\isometric tiles\Grid Labels\Acell.png").convert_alpha()
tile_10 = pygame.image.load("images\isometric tiles\Grid Labels\Acell.png").convert_alpha()

# import boat/grid assets
destroyer1_tile = pygame.image.load("images\isometric tiles\destroyer1.png").convert_alpha()
destroyer2_tile = pygame.image.load("images\isometric tiles\destroyer2.png").convert_alpha()
destroyerX_tile = pygame.image.load("images\isometric tiles\destroyerX.png").convert_alpha()
destroyerC_tile = pygame.image.load("images\isometric tiles\destroyerC.png").convert_alpha()

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
battleship3_tile = pygame.image.load("images\isometric tiles/bttlship3.png").convert_alpha()
battleship4_tile = pygame.image.load("images\isometric tiles/bttlship4.png").convert_alpha()
battleshipC_tile = pygame.image.load("images\isometric tiles/bttlshipC.png").convert_alpha()
battleshipX_tile = pygame.image.load("images\isometric tiles/bttlshipX.png").convert_alpha()

carrier1_tile = pygame.image.load("images\isometric tiles\carrier1.png").convert_alpha()
carrier2_tile = pygame.image.load("images\isometric tiles\carrier2.png").convert_alpha()
carrier3_tile = pygame.image.load("images\isometric tiles\carrier3.png").convert_alpha()
carrier4_tile = pygame.image.load("images\isometric tiles\carrier4.png").convert_alpha()
carrierC_tile = pygame.image.load("images\isometric tiles\carrierC.png").convert_alpha()
carrierX_tile = pygame.image.load("images\isometric tiles\carrierX.png").convert_alpha()

game_screen = "options"

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

PlacingGrid = [
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
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
BoatRotation = [0, 0, 0, 0, 0]

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
store_cd = 0

destroyer: dict = {0: destroyer2_tile,
                    1: destroyer1_tile
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

    screen.fill((100, 100, 100))
    placementGrid.fill((100, 100, 100))
    P1Grid.fill((100, 100, 100))
    P2Grid.fill((100, 100, 100))

    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    if game_screen == "options":
        switch("boat placing")
        selected_boat = 5
        cur_boat_len = 0
        selected_cell = pygame.Vector2(10,10)
        mov_cd = 0

    elif game_screen == "boat placing":
        xdil = 16
        ydil = 8
        # render grid labels
        for y, row in enumerate(PlacingGrid):
            if y == 0:
                for x, tile in enumerate(row):
                    tiles: dict = {0: "blank",
                                   1: tile_1,
                                   2: tile_2,
                                   3: tile_3,
                                   4: tile_4,
                                   5: tile_5,
                                   6: tile_6,
                                   7: tile_7,
                                   8: tile_8,
                                   9: tile_9,
                                   10: tile_10
                                   }
                    tile_sprite = tiles.get(x, "blank")
                    try:
                        placementGrid.blit(pygame.transform.scale_by(tile_sprite, 1), (170+(x-1)*xdil-(y-1.5)*xdil, 0+(x-1)*ydil+(y-1.5)*ydil))
                    except:
                        pass
            x = 0
            tiles: dict = {0: "blank",
                           1: tile_J,
                           2: tile_I,
                           3: tile_H,
                           4: tile_G,
                           5: tile_F,
                           6: tile_E,
                           7: tile_D,
                           8: tile_C,
                           9: tile_B,
                           10: tile_A
                            }
            tile_sprite = tiles.get(y, "blank")
            try:
                placementGrid.blit(pygame.transform.scale_by(tile_sprite, 1), (170+(x-1.5)*xdil-(y-1)*xdil, 0+(x-1.5)*ydil+(y-1)*ydil))
            except:
                pass
            

        for y, row in enumerate(PlacingGrid):
            for x, tile in enumerate(row):
                keys = pygame.key.get_pressed()


                if keys[pygame.K_1]:
                    selected_boat = 0
                    cur_boat_len = boat_len[selected_boat]
                    if StoredBoats[selected_boat] == 0:
                        for i, line in enumerate(PlacingGrid):
                            for j, cell in enumerate(line):
                                if PlacingGrid[j][i] == 10:
                                    selected_cell = pygame.Vector2(i, j)
                                    StoredBoats[selected_boat] = 1
                                if PlacingGrid[j][i] == 10 or PlacingGrid[j][i] == 11:
                                    PlacingGrid[j][i] = 00
                if keys[pygame.K_2]:
                    selected_boat = 1
                    cur_boat_len = boat_len[selected_boat]
                    if StoredBoats[selected_boat] == 0:
                        for i, line in enumerate(PlacingGrid):
                            for j, cell in enumerate(line):
                                if PlacingGrid[j][i] == 20:
                                    selected_cell = pygame.Vector2(i, j)
                                    StoredBoats[selected_boat] = 1
                                if PlacingGrid[j][i] == 20 or PlacingGrid[j][i] == 21 or PlacingGrid[j][i] == 22:
                                    PlacingGrid[j][i] = 00
                if keys[pygame.K_3]:
                    selected_boat = 2 
                    cur_boat_len = boat_len[selected_boat]
                    if StoredBoats[selected_boat] == 0:
                        for i, line in enumerate(PlacingGrid):
                            for j, cell in enumerate(line):
                                if PlacingGrid[j][i] == 30:
                                    selected_cell = pygame.Vector2(i, j)
                                    StoredBoats[selected_boat] = 1
                                if PlacingGrid[j][i] == 30 or PlacingGrid[j][i] == 31 or PlacingGrid[j][i] == 32:
                                    PlacingGrid[j][i] = 00
                if keys[pygame.K_4]:
                    selected_boat = 3
                    cur_boat_len = boat_len[selected_boat]
                    if StoredBoats[selected_boat] == 0:
                        for i, line in enumerate(PlacingGrid):
                            for j, cell in enumerate(line):
                                if PlacingGrid[j][i] == 40:
                                    selected_cell = pygame.Vector2(i, j)
                                    StoredBoats[selected_boat] = 1
                                if PlacingGrid[j][i] == 40 or PlacingGrid[j][i] == 41 or PlacingGrid[j][i] == 42 or PlacingGrid[j][i] == 43:
                                    PlacingGrid[j][i] = 00
                if keys[pygame.K_5]:
                    selected_boat = 4
                    cur_boat_len = boat_len[selected_boat]
                    if StoredBoats[selected_boat] == 0:
                        for i, line in enumerate(PlacingGrid):
                            for j, cell in enumerate(line):
                                if PlacingGrid[j][i] == 50:
                                    selected_cell = pygame.Vector2(i, j)
                                    StoredBoats[selected_boat] = 1
                                if PlacingGrid[j][i] == 50 or PlacingGrid[j][i] == 51 or PlacingGrid[j][i] == 52 or PlacingGrid[j][i] == 53 or PlacingGrid[j][i] == 54:
                                    PlacingGrid[j][i] = 00
                
                if selected_boat != 5 and selected_cell == (10, 10):
                    selected_cell = pygame.Vector2(0, 0)

                if mov_cd <= 0 and selected_cell != (10, 10):
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
                
                if store_cd <= 0 and keys[pygame.K_f]:
                    for i, line in enumerate(PlacingGrid):
                        for j, cell in enumerate(line):
                            if selected_boat == 0:
                                if PlacingGrid[j][i] == 10 or PlacingGrid[j][i] == 11:
                                    PlacingGrid[j][i] = 00
                            if selected_boat == 1:
                                if PlacingGrid[j][i] == 20 or PlacingGrid[j][i] == 21 or PlacingGrid[j][i] == 22:
                                    PlacingGrid[j][i] = 00
                            if selected_boat == 2:
                                if PlacingGrid[j][i] == 30 or PlacingGrid[j][i] == 31 or PlacingGrid[j][i] == 32:
                                    PlacingGrid[j][i] = 00
                            if selected_boat == 3:
                                if PlacingGrid[j][i] == 40 or PlacingGrid[j][i] == 41 or PlacingGrid[j][i] == 42 or PlacingGrid[j][i] == 43:
                                    PlacingGrid[j][i] = 00
                            if selected_boat == 4:
                                if PlacingGrid[j][i] == 50 or PlacingGrid[j][i] == 51 or PlacingGrid[j][i] == 52 or PlacingGrid[j][i] == 53 or PlacingGrid[j][i] == 54:
                                    PlacingGrid[j][i] = 00
                            if selected_boat == 5:
                                pass
                    if selected_boat != 5:
                        StoredBoats[selected_boat] = 1
                        selected_boat = 5
                        selected_cell = pygame.Vector2(10, 10)
                        for i, line in enumerate(PlacingGrid):
                            for j, cell in enumerate(line):
                                if PlacingGrid[j][i] == (10*e+10):
                                    selected_cell = pygame.Vector2(i, j)
                                if PlacingGrid[j][i] >= (10*e+10) and PlacingGrid[j][i] <= (10*e+15):
                                    PlacingGrid[j][i] = 00
                        cur_boat_len = boat_len[selected_boat]

                        store_cd = 15
                            
                
                if rot_cd <= 0 and keys[pygame.K_r]:
                    cursor_dir = cursor_dir*(-1) + 1
                    rot_cd = 15

                if x == selected_cell.x and y == selected_cell.y:
                    for i in range(0, cur_boat_len):
                        if cursor_dir == 0 and PlacingGrid[y][x+i] != 00:
                            bad_cell = True
                        if cursor_dir == 1 and PlacingGrid[y+i][x] != 00:
                            bad_cell = True
                else:
                    bad_cell = False
                
                funcs: dict = {00: d_sea_tile,
                            10: destroyer2_tile,
                            11: destroyer1_tile,
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
                    
                funcs: dict = {d_sea_tile: 00,
                            destroyer2_tile: 10,
                            destroyer1_tile: 11,
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
                    if selected_boat == 5:
                        break
                    for i, line in enumerate(PlacingGrid):
                        for j, cell in enumerate(line):
                            for e in range(1, cur_boat_len + 1):
                                if i == selected_cell.x and j == selected_cell.y:
                                    if cursor_dir == 0 and PlacingGrid[j][i+e-1] != 00:
                                        bad_cell = True
                                    if cursor_dir == 1 and PlacingGrid[j+e-1][i] != 00:
                                        bad_cell = True
                            if bad_cell == False:
                                for e in range(1, cur_boat_len + 1):
                                    if cursor_dir == 0 and (i == selected_cell.x + e - 1) and (j == selected_cell.y):
                                        PlacingGrid[j][i] = funcs.get(boats.get(selected_boat).get(e - 1), 99)
                                        BoatRotation[selected_boat] = 0
                                    if cursor_dir == 1 and (i == selected_cell.x) and (j == selected_cell.y + e - 1):
                                        PlacingGrid[j][i] = funcs.get(boats.get(selected_boat).get(e - 1), 99)
                                        BoatRotation[selected_boat] = 1
                    if bad_cell == False:
                        StoredBoats[selected_boat] = 0
                        i = 0
                        store_clear = True
                        for boat in StoredBoats:
                            if boat == 1:
                                selected_boat = i
                                store_clear = False
                                break
                            i += 1
                        if store_clear == True:
                            selected_boat = 5
                            selected_cell = pygame.Vector2(10, 10)
                        cur_boat_len = boat_len[selected_boat]
                        stamp_cd = 15
                
                boat_type = 9  
                rotate_cell = None              
                if (tile == 10) or (tile == 11):
                    boat_type = 0
                if (tile == 20) or (tile == 21) or (tile == 22):
                    boat_type = 1
                if (tile == 30) or (tile == 31) or (tile == 32):
                    boat_type = 2
                if (tile == 40) or (tile == 41) or (tile == 42) or (tile == 43):
                    boat_type = 3
                if (tile == 50) or (tile == 51) or (tile == 52) or (tile == 53) or (tile == 54):
                    boat_type = 4
                
                if boat_type != 9:
                    if BoatRotation[boat_type] == 0:
                        rotate_cell = False
                    elif BoatRotation[boat_type] == 1:
                        rotate_cell = True
                                    
                
                if (x == selected_cell.x) and (y == selected_cell.y):
                    if (((cursor_dir == 0) and (selected_cell.x + cur_boat_len < 11)) or ((cursor_dir == 1) and (selected_cell.y + cur_boat_len < 11))) and bad_cell == False:
                        funcs: dict = {0: destroyerC_tile,
                                1: subC_tile,
                                2: cruiserC_tile,
                                3: battleshipC_tile,
                                4: carrierC_tile
                                }
                    else:
                        funcs: dict = {0: destroyerX_tile,
                                1: subX_tile,
                                2: cruiserX_tile,
                                3: battleshipX_tile,
                                4: carrierX_tile
                                }
                    tile_sprite = funcs.get(selected_boat, "blank")
                if cursor_dir == 0:
                    if (x >= selected_cell.x and x < (selected_cell.x + cur_boat_len)):
                        for i in range(1, cur_boat_len):
                            if y == selected_cell.y and x == selected_cell.x + i:
                                tile_sprite = boats.get(selected_boat).get(i)
                                if tile_sprite != "blank":
                                    if x > 9:
                                        tile_sprite.set_alpha(155)
                                    else:
                                        tile_sprite.set_alpha(255)

                else:
                    if (y >= selected_cell.y and y < (selected_cell.y + cur_boat_len)):
                        for i in range(1, cur_boat_len):
                            if x == selected_cell.x and y == selected_cell.y + i:
                                tile_sprite = boats.get(selected_boat).get(i)
                                if tile_sprite != "blank":
                                    if y > 9:
                                        tile_sprite.set_alpha(155)
                                    else:
                                        tile_sprite.set_alpha(255)
                # render playing board
                if tile_sprite == "blank":
                    pass
                elif rotate_cell == False:
                    placementGrid.blit(tile_sprite, (170+x*xdil-y*xdil, 0+x*ydil+y*ydil))
                elif rotate_cell == True:
                    placementGrid.blit(pygame.transform.flip(tile_sprite, True, False), (170+x*xdil-y*xdil, 0+x*ydil+y*ydil))
                elif tile_sprite == d_sea_tile or cursor_dir == 0:
                    placementGrid.blit(tile_sprite, (170+x*xdil-y*xdil, 0+x*ydil+y*ydil))
                else:
                    placementGrid.blit(pygame.transform.flip(tile_sprite, True, False), (170+x*xdil-y*xdil, 0+x*ydil+y*ydil))
        
        mov_cd -= 1
        rot_cd -= 1
        swap_cd -= 1
        stamp_cd -=1
        store_cd -=1

        destroyer_indicator_P = button.Button(200, 100, lbl_destroyer_placed, 1)
        destroyer_indicator_S = button.Button(200, 100, lbl_destroyer_stored, 1)
        sub_indicator_S = button.Button(200, 200, lbl_sub_stored, 1)
        sub_indicator_P = button.Button(200, 200, lbl_sub_placed, 1)
        cruiser_indicator_S = button.Button(200, 300, lbl_cruiser_stored, 1)
        cruiser_indicator_P = button.Button(200, 300, lbl_cruiser_placed, 1)
        battleship_indicator_S = button.Button(200, 400, lbl_battleship_stored, 1)
        battleship_indicator_P = button.Button(200, 400, lbl_battleship_placed, 1)
        carrier_indicator_S = button.Button(200, 500, lbl_carrier_stored, 1)
        carrier_indicator_P = button.Button(200, 500, lbl_carrier_placed, 1)

        for i in range(len(StoredBoats)):
            j = i * 2 + StoredBoats[i]
            funcs: dict = {0: destroyer_indicator_P,
                           1: destroyer_indicator_S,
                           2: sub_indicator_P,
                           3: sub_indicator_S,
                           4: cruiser_indicator_P,
                           5: cruiser_indicator_S,
                           6: battleship_indicator_P,
                           7: battleship_indicator_S,
                           8: carrier_indicator_P,
                           9: carrier_indicator_S
                           }
            drawn_label = funcs.get(j, 0)
            drawn_label.draw(hud)

        confirmFleet_button = button.Button(1050, 650, confirmFleet_img, 3, confirmFleet_hover)
        if confirmFleet_button.draw(hud):
            if StoredBoats == [0, 0, 0, 0, 0]:
                switch("game")
            else:
                pygame.mixer.Sound.play(denyClick_sfx1)
        
    elif game_screen == "game":
        hud.fill((0, 0, 0, 0))
        for y, row in enumerate(PlacingGrid):
            for x, tile in enumerate(row):
                xdil = 16
                ydil = 8
                # pygame.draw.rect(display, (255, 255, 255), pygame.Rect(x*10, y*10, 10, 10), 1)
                funcs: dict = {00: d_sea_tile,
                            10: destroyer2_tile,
                            11: destroyer1_tile,
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
                tile_sprite = funcs.get(tile, d_sea_tile)
                display.blit(tile_sprite, (150+x*xdil-y*xdil, 0+x*ydil+y*ydil))
    
    # animate water
    if sea_anim_cd <= 0:
        cur_sea += 1
        if cur_sea == 3:
            cur_sea = 0
        tiles: list = [sea_tile,
                       sea_tile2,
                       sea_tile3
        ]
        d_sea_tile = tiles[cur_sea]
        sea_anim_cd = 15
    
    sea_anim_cd -= 1
    
    dt = clock.tick(60) / 1000
    screen.blit(pygame.transform.scale(placementGrid, (screen.get_width()/1.2, screen.get_width()/1.2)), (450,50))
    screen.blit(hud, (0, 0))
    pygame.display.update()

pygame.quit()