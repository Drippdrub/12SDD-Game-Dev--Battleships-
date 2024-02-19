import pygame
import sys
import os
import customwidgets as widgets
import random
from tkinter import *
from tkinter import messagebox
import copy
Tk().wm_withdraw() #to hide the main window

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

pygame.init()
pygame.display.set_caption("barebones")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32)
hud = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA, 32).convert_alpha()
leftRender = pygame.Surface((320, 320)).convert_alpha()
rightRender = pygame.Surface((320, 320)).convert_alpha()
placementSurface = pygame.Surface((400, 400)).convert_alpha()

clock = pygame.time.Clock()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    hud.blit(img, (x, y))

font1 = pygame.font.Font("fonts\CompassPro.ttf", 72)

place_sfx1 = pygame.mixer.Sound(resource_path("sounds\SFX\place.wav"))
place_sfx1.set_volume(0.75)
denyClick_sfx1 = pygame.mixer.Sound(resource_path("sounds/SFX/DenyClick.wav"))
denyClick_sfx1.set_volume(0.75)

playButton_img = pygame.image.load(resource_path("images/button_play.png")).convert_alpha()
playButton_hover = pygame.image.load(resource_path("images/button_play_hover.png")).convert_alpha()
okayButton_img = pygame.image.load(resource_path("images/button_okay.png")).convert_alpha()
okayButton_hover = pygame.image.load(resource_path("images/button_okay_hover.png")).convert_alpha()
okayButton_disabled = pygame.image.load(resource_path("images/button_okay_disabled.png")).convert_alpha()
select1P_img = pygame.image.load(resource_path("images/toggle_select1P.png")).convert_alpha()
select2P_img = pygame.image.load(resource_path("images/toggle_select2P.png")).convert_alpha()
confirmFleet_img = pygame.image.load(resource_path("images/button_confirmfleet.png")).convert_alpha()
confirmFleet_hover = pygame.image.load(resource_path("images/button_confirmfleet_hover.png")).convert_alpha()
randomiseFleet_img = pygame.image.load(resource_path("images/button_randomisefleet.png")).convert_alpha()
randomiseFleet_hover = pygame.image.load(resource_path("images/button_randomisefleet_hover.png")).convert_alpha()

nuke_img = pygame.image.load(resource_path("images/nuke.png")).convert_alpha()

# iso_test = pygame.image.load(resource_path("images\iso_test.png")).convert_alpha()
# ship_tile = pygame.image.load(resource_path("images\isometric tiles\ship unit.png")).convert_alpha()

lbl_destroyer_stored = pygame.image.load(resource_path("images\Placement Labels\DestroyerStored.png")).convert_alpha()
lbl_destroyer_placed = pygame.image.load(resource_path("images\Placement Labels\DestroyerPlaced.png")).convert_alpha()
lbl_sub_stored = pygame.image.load(resource_path("images\Placement Labels\SubmarineStored.png")).convert_alpha()
lbl_sub_placed = pygame.image.load(resource_path("images\Placement Labels\SubmarinePlaced.png")).convert_alpha()
lbl_cruiser_stored = pygame.image.load(resource_path("images\Placement Labels\CruiserStored.png")).convert_alpha()
lbl_cruiser_placed = pygame.image.load(resource_path("images\Placement Labels\CruiserPlaced.png")).convert_alpha()
lbl_battleship_stored = pygame.image.load(resource_path("images\Placement Labels\BattleshipStored.png")).convert_alpha()
lbl_battleship_placed = pygame.image.load(resource_path("images\Placement Labels\BattleshipPlaced.png")).convert_alpha()
lbl_carrier_stored = pygame.image.load(resource_path("images\Placement Labels\CarrierStored.png")).convert_alpha()
lbl_carrier_placed = pygame.image.load(resource_path("images\Placement Labels\CarrierPlaced.png")).convert_alpha()

# import sea assets
sea_anim_cd = 0
cur_sea = 0
d_sea_tile = pygame.image.load(resource_path("images\isometric tiles\sea unit.png")).convert_alpha()
fake_sea_tile = pygame.image.load(resource_path("images\isometric tiles\sea unit.png")).convert_alpha()
sea_tile1 = pygame.image.load(resource_path("images\isometric tiles\sea unit.png")).convert_alpha()
sea_tile2 = pygame.image.load(resource_path("images\isometric tiles\sea unit2.png")).convert_alpha()
sea_tile3 = pygame.image.load(resource_path("images\isometric tiles\sea unit3.png")).convert_alpha()

# import grid cell labels
tile_A = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Acell.png")).convert_alpha()
tile_B = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Bcell.png")).convert_alpha()
tile_C = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Ccell.png")).convert_alpha()
tile_D = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Dcell.png")).convert_alpha()
tile_E = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Ecell.png")).convert_alpha()
tile_F = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Fcell.png")).convert_alpha()
tile_G = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Gcell.png")).convert_alpha()
tile_H = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Hcell.png")).convert_alpha()
tile_I = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Icell.png")).convert_alpha()
tile_J = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Jcell.png")).convert_alpha()
tile_1 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Acell.png")).convert_alpha()
tile_2 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Acell.png")).convert_alpha()
tile_3 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Acell.png")).convert_alpha()
tile_4 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Acell.png")).convert_alpha()
tile_5 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Acell.png")).convert_alpha()
tile_6 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Acell.png")).convert_alpha()
tile_7 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Acell.png")).convert_alpha()
tile_8 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Acell.png")).convert_alpha()
tile_9 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Acell.png")).convert_alpha()
tile_10 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Acell.png")).convert_alpha()

# import boat/grid assets
destroyer1_tile = pygame.image.load(resource_path("images\isometric tiles\destroyer1.png")).convert_alpha()
destroyer2_tile = pygame.image.load(resource_path("images\isometric tiles\destroyer2.png")).convert_alpha()
destroyerX_tile = pygame.image.load(resource_path("images\isometric tiles\destroyerX.png")).convert_alpha()
destroyerC_tile = pygame.image.load(resource_path("images\isometric tiles\destroyerC.png")).convert_alpha()

sub1_tile = pygame.image.load(resource_path("images\isometric tiles\sub1.png")).convert_alpha()
sub2_tile = pygame.image.load(resource_path("images\isometric tiles\sub2.png")).convert_alpha()
sub3_tile = pygame.image.load(resource_path("images\isometric tiles\sub3.png")).convert_alpha()
subX_tile = pygame.image.load(resource_path("images\isometric tiles\subX.png")).convert_alpha()
subC_tile = pygame.image.load(resource_path("images\isometric tiles\subC.png")).convert_alpha()

cruiser1_tile = pygame.image.load(resource_path("images\isometric tiles\cruiser1.png")).convert_alpha()
cruiser2_tile = pygame.image.load(resource_path("images\isometric tiles\cruiser2.png")).convert_alpha()
cruiser3_tile = pygame.image.load(resource_path("images\isometric tiles\cruiser3.png")).convert_alpha()
cruiserX_tile = pygame.image.load(resource_path("images\isometric tiles\cruiserX.png")).convert_alpha()
cruiserC_tile = pygame.image.load(resource_path("images\isometric tiles\cruiserC.png")).convert_alpha()

battleship1_tile = pygame.image.load(resource_path("images\isometric tiles/bttlship1.png")).convert_alpha()
battleship2_tile = pygame.image.load(resource_path("images\isometric tiles/bttlship2.png")).convert_alpha()
battleship3_tile = pygame.image.load(resource_path("images\isometric tiles/bttlship3.png")).convert_alpha()
battleship4_tile = pygame.image.load(resource_path("images\isometric tiles/bttlship4.png")).convert_alpha()
battleshipC_tile = pygame.image.load(resource_path("images\isometric tiles/bttlshipC.png")).convert_alpha()
battleshipX_tile = pygame.image.load(resource_path("images\isometric tiles/bttlshipX.png")).convert_alpha()

carrier1_tile = pygame.image.load(resource_path("images\isometric tiles\carrier1.png")).convert_alpha()
carrier2_tile = pygame.image.load(resource_path("images\isometric tiles\carrier2.png")).convert_alpha()
carrier3_tile = pygame.image.load(resource_path("images\isometric tiles\carrier3.png")).convert_alpha()
carrier4_tile = pygame.image.load(resource_path("images\isometric tiles\carrier4.png")).convert_alpha()
carrierC_tile = pygame.image.load(resource_path("images\isometric tiles\carrierC.png")).convert_alpha()
carrierX_tile = pygame.image.load(resource_path("images\isometric tiles\carrierX.png")).convert_alpha()

game_screen = "options"

BlankGrid = [
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
PlacingGrid = []
P1Boats = []
P2Boats = []

def switch(screen):
    global game_screen
    game_screen = screen
    print(screen)

selectedPlayerMode = True

inGame = False
playersReady = 0

prompt_cd = 0

StoredBoats = [1, 1, 1, 1, 1]
BoatRotation = [0, 0, 0, 0, 0]
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

P1Rot = []
P2Rot = []

turn = 0
anim_ticks = 0
left_size = 0
right_size = 0
left_pos = pygame.Vector2(0, 0)
right_pos = pygame.Vector2(0, 0)

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

# options widgets
selectPlayer = widgets.Toggle(640, 300, select1P_img, select2P_img, 1.5)
optionsProceed = widgets.Button(640, 420, playButton_img, 3, playButton_hover)

# prompt widgets
promptDisabled = widgets.Image(640, 420, okayButton_disabled, 3)
promptProceed = widgets.Button(640, 420, okayButton_img, 3, okayButton_hover)
gameBegin = widgets.Button(640, 420, playButton_img, 3, playButton_hover)

# boat placement widgets
destroyer_indicator_P = widgets.Image(200, 100, lbl_destroyer_placed, 1)
destroyer_indicator_S = widgets.Image(200, 100, lbl_destroyer_stored, 1)
sub_indicator_S = widgets.Image(200, 200, lbl_sub_stored, 1)
sub_indicator_P = widgets.Image(200, 200, lbl_sub_placed, 1)
cruiser_indicator_S = widgets.Image(200, 300, lbl_cruiser_stored, 1)
cruiser_indicator_P = widgets.Image(200, 300, lbl_cruiser_placed, 1)
battleship_indicator_S = widgets.Image(200, 400, lbl_battleship_stored, 1)
battleship_indicator_P = widgets.Image(200, 400, lbl_battleship_placed, 1)
carrier_indicator_S = widgets.Image(200, 500, lbl_carrier_stored, 1)
carrier_indicator_P = widgets.Image(200, 500, lbl_carrier_placed, 1)

confirmFleet_button = widgets.Button(1050, 650, confirmFleet_img, 3, confirmFleet_hover)
randomiseFleet_button = widgets.Button(600, 650, randomiseFleet_img, 3, randomiseFleet_hover)

running = True
while running:

    screen.fill((100, 100, 100))
    placementSurface.fill((0, 0, 0, 0))
    hud.fill((0, 0, 0, 0))
    # leftRender.fill((0, 0, 0, 0))
    # rightRender.fill((0, 0, 0, 0))
    leftRender.fill((176, 11, 19, 150))
    rightRender.fill((42, 6, 90, 150))

    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    if game_screen == "options":
        selectedPlayerMode = selectPlayer.draw(hud, output=0)
        if optionsProceed.draw(hud):
            switch("page router")
    
    elif game_screen == "page router":
        if inGame == False:
            selected_boat = 5
            cur_boat_len = 0
            selected_cell = pygame.Vector2(10,10)
            mov_cd = 0
            rot_cd = 0
            cursor_dir = 0
            swap_cd = 0
            bad_cell = False
            stamp_cd = 0
            store_cd = 0
            StoredBoats = [1, 1, 1, 1, 1]
            prompt_cd = 60
            if selectedPlayerMode == False: #if 1 player mode was selected
                if playersReady == 0:
                    playersReady = 1
                    switch("P1Prompt")
                elif playersReady == 1:
                    P1Boats = PlacingGrid
                    P1Rot = BoatRotation
                    playersReady = 2
                    switch("AIPrep")
            else:
                if playersReady == 0:
                    playersReady = 1
                    switch("P1Prompt")
                elif playersReady == 1:
                    P1Boats = PlacingGrid
                    P1Rot = BoatRotation
                    playersReady = 2
                    switch("P2Prompt")
                elif playersReady == 2:
                    P2Boats = PlacingGrid
                    P2Rot = BoatRotation
                    playersReady = 3
                    switch("GameReady")
            BoatRotation = [0, 0, 0, 0, 0]
            PlacingGrid = copy.deepcopy(BlankGrid)
        else:
            if turn == 1:
                anim_ticks = 0
                switch("P1Game")
            else:
                if selectedPlayerMode == False:
                    pass
                else:
                    if turn % 2 == 1:
                        pass
                    else:
                        pass
    
    elif game_screen == "P1Prompt":
        if selectedPlayerMode == False:
            draw_text("Place down your ships", font1, (0, 0, 0), (1280-font1.size("Place down your ships")[0])/2, 100)
        else:
            draw_text("Pass this device to Player 1", font1, (0, 0, 0), (1280-font1.size("Pass this device to Player 1")[0])/2, 100)
        if prompt_cd <= 0:
            if promptProceed.draw(hud):
                switch("boat placing")
        else:
            promptDisabled.draw(hud)
        prompt_cd -= 1
    
    elif game_screen == "P2Prompt":
        draw_text("Pass this device to Player 2", font1, (0, 0, 0), (1280-font1.size("Pass this device to Player 2")[0])/2, 100)
        if prompt_cd <= 0:
            if promptProceed.draw(hud):
                switch("boat placing")
        else:
            promptDisabled.draw(hud)
        prompt_cd -= 1

    elif game_screen == "AIPrep":
        boat_count = 6
        for boat in [5, 4, 3, 3, 2]:
            boat_count -= 1
            bad_cell = True
            while bad_cell:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                rot = random.randint(0, 1)
                bad_cell = False
                cur_boat_len = boat
                for i in range(0, cur_boat_len):
                        if rot == 0 and PlacingGrid[y][x+i] != 00:
                            bad_cell = True
                        if rot == 1 and PlacingGrid[y+i][x] != 00:
                            bad_cell = True
                if bad_cell == False:
                    for e in range(0, cur_boat_len):
                        if rot == 0:
                            PlacingGrid[y][x+e] = boat_count*10 + e
                            BoatRotation[boat_count - 1] = 0
                        if rot == 1:
                            PlacingGrid[y+e][x] = boat_count*10 + e
                            BoatRotation[boat_count - 1] = 1

        P2Boats = PlacingGrid
        P2Rot = BoatRotation
        switch("AIReady")

    elif game_screen == "AIReady":
        draw_text("Start Game", font1, (0, 0, 0), (1280-font1.size("Start Game")[0])/2, 100)
        if gameBegin.draw(hud):
            inGame = True
            turn = 1
            switch("page router")

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
                        placementSurface.blit(tile_sprite, (183+(x-1)*xdil-(y-1.5)*xdil, 0+(x-1)*ydil+(y-1.5)*ydil))
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
                placementSurface.blit(tile_sprite, (183+(x-1.5)*xdil-(y-1)*xdil, 0+(x-1.5)*ydil+(y-1)*ydil))
            except:
                pass
            
        # render board grid
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
                    if selected_boat != 5:
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
                            pygame.mixer.Sound.play(place_sfx1)
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
                                tile_sprite = boats.get(selected_boat).get(i, "blank")
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
                    placementSurface.blit(tile_sprite, (183+x*xdil-y*xdil, 0+x*ydil+y*ydil))
                elif rotate_cell == True:
                    placementSurface.blit(pygame.transform.flip(tile_sprite, True, False), (183+x*xdil-y*xdil, 0+x*ydil+y*ydil))
                elif tile_sprite == d_sea_tile or cursor_dir == 0:
                    placementSurface.blit(tile_sprite, (183+x*xdil-y*xdil, 0+x*ydil+y*ydil))
                else:
                    placementSurface.blit(pygame.transform.flip(tile_sprite, True, False), (183+x*xdil-y*xdil, 0+x*ydil+y*ydil))
        
        mov_cd -= 1
        rot_cd -= 1
        swap_cd -= 1
        stamp_cd -=1
        store_cd -=1

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

        if randomiseFleet_button.draw(hud):
            boat_count = 6
            PlacingGrid = copy.deepcopy(BlankGrid)
            for boat in [5, 4, 3, 3, 2]:
                boat_count -= 1
                bad_cell = True
                while bad_cell:
                    x = random.randint(0, 9)
                    y = random.randint(0, 9)
                    rot = random.randint(0, 1)
                    bad_cell = False
                    cur_boat_len = boat
                    for i in range(0, cur_boat_len):
                            if rot == 0 and PlacingGrid[y][x+i] != 00:
                                bad_cell = True
                            if rot == 1 and PlacingGrid[y+i][x] != 00:
                                bad_cell = True
                    if bad_cell == False:
                        for e in range(0, cur_boat_len):
                            if rot == 0:
                                PlacingGrid[y][x+e] = boat_count*10 + e
                                BoatRotation[boat_count - 1] = 0
                            if rot == 1:
                                PlacingGrid[y+e][x] = boat_count*10 + e
                                BoatRotation[boat_count - 1] = 1
                selected_boat = 5
                cur_boat_len = 0
                selected_cell = pygame.Vector2(10,10)
                mov_cd = 0
                rot_cd = 0
                cursor_dir = 0
                swap_cd = 0
                bad_cell = False
                stamp_cd = 0
                store_cd = 0
                StoredBoats = [0, 0, 0, 0, 0]

        if confirmFleet_button.draw(hud):
            if StoredBoats == [0, 0, 0, 0, 0]:
                if messagebox.askokcancel("Confirm Boat Placement", "Your boats will be locked in place for the rest of the game.\nDo you wish to continue?"):
                    switch("page router")
            else:
                pygame.mixer.Sound.play(denyClick_sfx1)
    
    elif game_screen == "GameReady":
        draw_text("Start Game", font1, (0, 0, 0), (1280-font1.size("Start Game")[0])/2, 100)
        if gameBegin.draw(hud):
            inGame = True
            turn = 1
            switch("page router")

    elif game_screen == "P1Game":
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
                            54: carrier1_tile,
                            99: "blank"
                            }
        # left render
        for y, row in enumerate(P2Boats):
            for x, tile in enumerate(row):
                xdil = 16
                ydil = 8
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
                    if P2Rot[boat_type] == 0:
                        rotate_cell = False
                    elif P2Rot[boat_type] == 1:
                        rotate_cell = True

                if tile in [10, 11, 20, 21, 22, 30, 31, 32, 40, 41, 42, 43, 50, 51, 52, 53, 54] and not keys[pygame.K_f]:
                    tile_sprite = d_sea_tile
                else:
                    tile_sprite = funcs.get(tile, d_sea_tile)

                if tile_sprite == "blank":
                    pass
                elif rotate_cell == False:
                    leftRender.blit(tile_sprite, (144+x*xdil-y*xdil, -32+x*ydil+y*ydil))
                else:
                    leftRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, -32+x*ydil+y*ydil))

        # right render
        for y, row in enumerate(P1Boats):
            for x, tile in enumerate(row):
                xdil = 16
                ydil = 8
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
                    if P1Rot[boat_type] == 0:
                        rotate_cell = False
                    elif P1Rot[boat_type] == 1:
                        rotate_cell = True
                
                tile_sprite = funcs.get(tile, d_sea_tile)

                if tile_sprite == "blank":
                    pass
                elif rotate_cell == False:
                    rightRender.blit(tile_sprite, (144+x*xdil-y*xdil, -32+x*ydil+y*ydil))
                else:
                    rightRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, -32+x*ydil+y*ydil))
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_e]:
            anim_ticks = 0

        t = 30
        scale = 10
        diff = 1.5
        delay = 90
        if anim_ticks <= delay:
            left_size = screen.get_width()/2 + scale*(1 - (0.5*t)*diff)
            right_size = screen.get_width()/2 + scale*(1 + (0.5*t)*diff)
            left_pos = pygame.Vector2(50, 50)
            right_pos = pygame.Vector2(1230-right_size, 670-(right_size*0.55))
            anim_ticks += 1
        elif delay < anim_ticks <= delay + t:
            left_size = screen.get_width()/2 + scale*(1 - (0.5*t - (anim_ticks - delay))*diff)
            right_size = screen.get_width()/2 + scale*(1 + (0.5*t - (anim_ticks - delay))*diff)
            left_pos = pygame.Vector2(50, 50)
            right_pos = pygame.Vector2(1230-right_size, 670-(right_size*0.55))
            anim_ticks += 1

    # animate water
    if sea_anim_cd <= 0:
        cur_sea += 1
        if cur_sea == 3:
            cur_sea = 0
        tiles: list = [sea_tile1,
                       sea_tile2,
                       sea_tile3
        ]
        d_sea_tile = tiles[cur_sea]
        sea_anim_cd = 15
    
    sea_anim_cd -= 1
    
    dt = clock.tick(60) / 1000
    screen.blit(pygame.transform.scale(placementSurface, (screen.get_width()/1.4, screen.get_width()/1.4)), (380, 50))
    screen.blit(pygame.transform.scale(leftRender, (left_size, left_size)), left_pos)
    screen.blit(pygame.transform.scale(rightRender, (right_size, right_size)), right_pos)
    screen.blit(hud, (0, 0))
    
    pygame.display.update()

pygame.quit()