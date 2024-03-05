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
import volume_slider as slider 

Tk().wm_withdraw() #to hide the main window

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

font1 = pygame.font.Font(resource_path("fonts\CompassPro.ttf"), 72)
font2 = pygame.font.Font(resource_path("fonts\Crang.ttf"), 84)

master_lvl = 1.0
sfx_lvl = 0.75
music_lvl = 0.75

startup_sfx1 = pygame.mixer.Sound(resource_path("sounds/SFX/Explosion1.wav"))
startup_sfx1.set_volume(0.75)
startup_sfx2 = pygame.mixer.Sound(resource_path("sounds\SFX\Blip1.wav"))
startup_sfx2.set_volume(0.75)
startup_jingle = pygame.mixer.Sound(resource_path("sounds\Music\weezer.wav"))
startup_jingle.set_volume(0.9)
startup_music = pygame.mixer.music.load(resource_path("sounds\\Music\\unending.wav"))

place_sfx1 = pygame.mixer.Sound(resource_path("sounds\SFX\place.wav"))
place_sfx1.set_volume(0.75)
denyClick_sfx1 = pygame.mixer.Sound(resource_path("sounds\SFX\DenyClick.wav"))
denyClick_sfx1.set_volume(0.75)

sink_sfx1 = pygame.mixer.Sound(resource_path("sounds\SFX\Sink.wav"))
sink_sfx1.set_volume(0.75)

explosion_sfx1 = pygame.mixer.Sound(resource_path("sounds\SFX\Explosion1.wav"))
explosion_sfx1.set_volume(0.75)
explosion_sfx2 = pygame.mixer.Sound(resource_path("sounds\SFX\Explosion2.wav"))
explosion_sfx2.set_volume(0.75)
explosion_sfx3 = pygame.mixer.Sound(resource_path("sounds\SFX\Explosion3.wav"))
explosion_sfx3.set_volume(0.75)
explosion_sfx4 = pygame.mixer.Sound(resource_path("sounds\SFX\Explosion4.wav"))
explosion_sfx4.set_volume(0.75)

splash_sfx1 = pygame.mixer.Sound(resource_path("sounds\SFX\Splash.wav"))
splash_sfx1.set_volume(0.75)
splash_sfx2 = pygame.mixer.Sound(resource_path("sounds\SFX\Splash2.wav"))
splash_sfx2.set_volume(0.75)
splash_sfx3 = pygame.mixer.Sound(resource_path("sounds\SFX\Splash3.wav"))
splash_sfx3.set_volume(0.75)
splash_sfx4 = pygame.mixer.Sound(resource_path("sounds\SFX\Splash4.wav"))
splash_sfx4.set_volume(0.75)
splash_sfx5 = pygame.mixer.Sound(resource_path("sounds\SFX\Splash5.wav"))
splash_sfx5.set_volume(0.75)

playButton_img = pygame.image.load(resource_path("images/button_play.png")).convert_alpha()
playButton_hover = pygame.image.load(resource_path("images/button_play_hover.png")).convert_alpha()
optionButton_img = pygame.image.load(resource_path("images/button_options.png")).convert_alpha()
optionButton_hover = pygame.image.load(resource_path("images/button_options_hover.png")).convert_alpha()
creditsButton_img = pygame.image.load(resource_path("images/button_credits.png")).convert_alpha()
creditsButton_hover = pygame.image.load(resource_path("images/button_credits_hover.png")).convert_alpha()
exitButton_img = pygame.image.load(resource_path("images/button_exit.png")).convert_alpha()
exitButton_hover = pygame.image.load(resource_path("images/button_exit_hover.png")).convert_alpha()
backButton_img = pygame.image.load(resource_path("images/button_back.png")).convert_alpha()
okayButton_img = pygame.image.load(resource_path("images/button_okay.png")).convert_alpha()
okayButton_hover = pygame.image.load(resource_path("images/button_okay_hover.png")).convert_alpha()
okayButton_disabled = pygame.image.load(resource_path("images/button_okay_disabled.png")).convert_alpha()
select1P_img = pygame.image.load(resource_path("images/toggle_select1P.png")).convert_alpha()
select2P_img = pygame.image.load(resource_path("images/toggle_select2P.png")).convert_alpha()
selectDiffEasy_img = pygame.image.load(resource_path("images/toggle_diffEasy.png")).convert_alpha()
selectDiffHard_img = pygame.image.load(resource_path("images/toggle_diffHard.png")).convert_alpha()
confirmFleet_img = pygame.image.load(resource_path("images/button_confirmfleet.png")).convert_alpha()
confirmFleet_hover = pygame.image.load(resource_path("images/button_confirmfleet_hover.png")).convert_alpha()
randomiseFleet_img = pygame.image.load(resource_path("images/button_randomisefleet.png")).convert_alpha()
randomiseFleet_hover = pygame.image.load(resource_path("images/button_randomisefleet_hover.png")).convert_alpha()

player1Board_img = pygame.image.load(resource_path("images\Player1 Board.png")).convert_alpha()
player2Board_img = pygame.image.load(resource_path("images\Player2 Board.png")).convert_alpha()
ai_easy_Board_img = pygame.image.load(resource_path("images\AI Easy Board.png")).convert_alpha()
ai_hard_Board_img = pygame.image.load(resource_path("images\AI Hard Board.png")).convert_alpha()
middle_Board_img = pygame.image.load(resource_path("images\Middle Board.png")).convert_alpha()
big_Board_img = pygame.image.load(resource_path("images\Big Board.png")).convert_alpha()

hud_P1P2_img = pygame.image.load(resource_path("images\Huds\Hud1.png")).convert_alpha()
hug_P2P1_img = pygame.image.load(resource_path("images\Huds\Hud4.png")).convert_alpha()
hud_P1A1_img = pygame.image.load(resource_path("images\Huds\Hud2.png")).convert_alpha()
hud_P1A2_img = pygame.image.load(resource_path("images\Huds\Hud3.png")).convert_alpha()

ocean_screen = pygame.image.load(resource_path("images/Ocean.png")).convert_alpha()

nuke_img = pygame.image.load(resource_path("images/nuke.png")).convert_alpha()

black_screen = pygame.image.load(resource_path("images/black_screen.png")).convert_alpha()
blast_door_1 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door1.png")).convert_alpha()
blast_door_2 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door2.png")).convert_alpha()
blast_door_3 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door3.png")).convert_alpha()
blast_door_4 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door4.png")).convert_alpha()
blast_door_5 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door5.png")).convert_alpha()
blast_door_6 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door6.png")).convert_alpha()
blast_door_7 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door7.png")).convert_alpha()
blast_door_8 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door8.png")).convert_alpha()

explosion_frame_1 = pygame.image.load(resource_path("images\Anims\Explosion/1.png")).convert_alpha()
explosion_frame_2 = pygame.image.load(resource_path("images\Anims\Explosion/2.png")).convert_alpha()
explosion_frame_3 = pygame.image.load(resource_path("images\Anims\Explosion/3.png")).convert_alpha()
explosion_frame_4 = pygame.image.load(resource_path("images\Anims\Explosion/4.png")).convert_alpha()
explosion_frame_5 = pygame.image.load(resource_path("images\Anims\Explosion/5.png")).convert_alpha()
explosion_frame_6 = pygame.image.load(resource_path("images\Anims\Explosion/6.png")).convert_alpha()
explosion_frame_7 = pygame.image.load(resource_path("images\Anims\Explosion/7.png")).convert_alpha()
explosion_frame_8 = pygame.image.load(resource_path("images\Anims\Explosion/8.png")).convert_alpha()
explosion_frame_9 = pygame.image.load(resource_path("images\Anims\Explosion/9.png")).convert_alpha()
explosion_frame_10 = pygame.image.load(resource_path("images\Anims\Explosion/10.png")).convert_alpha()
explosion_frame_11 = pygame.image.load(resource_path("images\Anims\Explosion/11.png")).convert_alpha()
explosion_frame_12 = pygame.image.load(resource_path("images\Anims\Explosion/12.png")).convert_alpha()

splash_frame_1 = pygame.image.load(resource_path("images\Anims\Splash/1.png")).convert_alpha()
splash_frame_2 = pygame.image.load(resource_path("images\Anims\Splash/2.png")).convert_alpha()
splash_frame_3 = pygame.image.load(resource_path("images\Anims\Splash/3.png")).convert_alpha()
splash_frame_4 = pygame.image.load(resource_path("images\Anims\Splash/4.png")).convert_alpha()
splash_frame_5 = pygame.image.load(resource_path("images\Anims\Splash/5.png")).convert_alpha()
splash_frame_6 = pygame.image.load(resource_path("images\Anims\Splash/6.png")).convert_alpha()
splash_frame_7 = pygame.image.load(resource_path("images\Anims\Splash/7.png")).convert_alpha()
splash_frame_8 = pygame.image.load(resource_path("images\Anims\Splash/8.png")).convert_alpha()
splash_frame_9 = pygame.image.load(resource_path("images\Anims\Splash/9.png")).convert_alpha()
splash_frame_10 = pygame.image.load(resource_path("images\Anims\Splash/10.png")).convert_alpha()
splash_frame_11 = pygame.image.load(resource_path("images\Anims\Splash/11.png")).convert_alpha()
splash_frame_12 = pygame.image.load(resource_path("images\Anims\Splash/12.png")).convert_alpha()

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
d_sea_nohit_tile = pygame.image.load(resource_path("images\isometric tiles\sea no_hit1.png")).convert_alpha()
d_sea_hit_tile = pygame.image.load(resource_path("images\isometric tiles\sea hit1.png")).convert_alpha()
sea_tile1 = pygame.image.load(resource_path("images\isometric tiles\sea unit.png")).convert_alpha()
sea_tile2 = pygame.image.load(resource_path("images\isometric tiles\sea unit2.png")).convert_alpha()
sea_tile3 = pygame.image.load(resource_path("images\isometric tiles\sea unit3.png")).convert_alpha()
sea_nohit_tile1 = pygame.image.load(resource_path("images\isometric tiles\sea no_hit1.png")).convert_alpha()
sea_nohit_tile2 = pygame.image.load(resource_path("images\isometric tiles\sea no_hit2.png")).convert_alpha()
sea_nohit_tile3 = pygame.image.load(resource_path("images\isometric tiles\sea no_hit3.png")).convert_alpha()
sea_hit_tile1 = pygame.image.load(resource_path("images\isometric tiles\sea hit1.png")).convert_alpha()
sea_hit_tile2 = pygame.image.load(resource_path("images\isometric tiles\sea hit2.png")).convert_alpha()
sea_hit_tile3 = pygame.image.load(resource_path("images\isometric tiles\sea hit3.png")).convert_alpha()

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
tile_1 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels/1cell.png")).convert_alpha()
tile_2 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels/2cell.png")).convert_alpha()
tile_3 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels/3cell.png")).convert_alpha()
tile_4 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels/4cell.png")).convert_alpha()
tile_5 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels/5cell.png")).convert_alpha()
tile_6 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels/6cell.png")).convert_alpha()
tile_7 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels/7cell.png")).convert_alpha()
tile_8 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels/8cell.png")).convert_alpha()
tile_9 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels/9cell.png")).convert_alpha()
tile_10 = pygame.image.load(resource_path("images\isometric tiles\Grid Labels/10cell.png")).convert_alpha()

# import boat/grid assets
cursorC = pygame.image.load(resource_path("images\isometric tiles\cursorC.png")).convert_alpha()
cursorX = pygame.image.load(resource_path("images\isometric tiles\cursorX.png")).convert_alpha()


destroyer1_tile = pygame.image.load(resource_path("images\isometric tiles\destroyer1.png")).convert_alpha()
destroyer2_tile = pygame.image.load(resource_path("images\isometric tiles\destroyer2.png")).convert_alpha()
destroyerX_tile = pygame.image.load(resource_path("images\isometric tiles\destroyerX.png")).convert_alpha()
destroyerC_tile = pygame.image.load(resource_path("images\isometric tiles\destroyerC.png")).convert_alpha()

destroyer1_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Destroyer\Destroyer1\Destroyer1_Sink1.png")).convert_alpha()
destroyer1_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Destroyer\Destroyer1\Destroyer1_Sink2.png")).convert_alpha()
destroyer1_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Destroyer\Destroyer1\Destroyer1_Sink3.png")).convert_alpha()
destroyer1_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Destroyer\Destroyer1\Destroyer1_Sink4.png")).convert_alpha()
destroyer1_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Destroyer\Destroyer1\Destroyer1_Sink5.png")).convert_alpha()

destroyer2_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Destroyer\Destroyer2/Destroyer2_Sink1.png")).convert_alpha()
destroyer2_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Destroyer\Destroyer2/Destroyer2_Sink2.png")).convert_alpha()
destroyer2_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Destroyer\Destroyer2/Destroyer2_Sink3.png")).convert_alpha()
destroyer2_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Destroyer\Destroyer2/Destroyer2_Sink4.png")).convert_alpha()
destroyer2_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Destroyer\Destroyer2/Destroyer2_Sink5.png")).convert_alpha()


sub1_tile = pygame.image.load(resource_path("images\isometric tiles\sub1.png")).convert_alpha()
sub2_tile = pygame.image.load(resource_path("images\isometric tiles\sub2.png")).convert_alpha()
sub3_tile = pygame.image.load(resource_path("images\isometric tiles\sub3.png")).convert_alpha()
subX_tile = pygame.image.load(resource_path("images\isometric tiles\subX.png")).convert_alpha()
subC_tile = pygame.image.load(resource_path("images\isometric tiles\subC.png")).convert_alpha()

submarine1_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine1\Submarine1_Sink1.png")).convert_alpha()
submarine1_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine1\Submarine1_Sink2.png")).convert_alpha()
submarine1_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine1\Submarine1_Sink3.png")).convert_alpha()
submarine1_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine1\Submarine1_Sink4.png")).convert_alpha()
submarine1_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine1\Submarine1_Sink5.png")).convert_alpha()

submarine2_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine2\Submarine2_Sink1.png")).convert_alpha()
submarine2_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine2\Submarine2_Sink2.png")).convert_alpha()
submarine2_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine2\Submarine2_Sink3.png")).convert_alpha()
submarine2_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine2\Submarine2_Sink4.png")).convert_alpha()
submarine2_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine2\Submarine2_Sink5.png")).convert_alpha()

submarine3_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine3\Submarine3_Sink1.png")).convert_alpha()
submarine3_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine3\Submarine3_Sink2.png")).convert_alpha()
submarine3_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine3\Submarine3_Sink3.png")).convert_alpha()
submarine3_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine3\Submarine3_Sink4.png")).convert_alpha()
submarine3_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Submarine\Submarine3\Submarine3_Sink5.png")).convert_alpha()


cruiser1_tile = pygame.image.load(resource_path("images\isometric tiles\cruiser1.png")).convert_alpha()
cruiser2_tile = pygame.image.load(resource_path("images\isometric tiles\cruiser2.png")).convert_alpha()
cruiser3_tile = pygame.image.load(resource_path("images\isometric tiles\cruiser3.png")).convert_alpha()
cruiserX_tile = pygame.image.load(resource_path("images\isometric tiles\cruiserX.png")).convert_alpha()
cruiserC_tile = pygame.image.load(resource_path("images\isometric tiles\cruiserC.png")).convert_alpha()

cruiser1_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser1\Cruiser1_Sink1.png")).convert_alpha()
cruiser1_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser1\Cruiser1_Sink2.png")).convert_alpha()
cruiser1_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser1\Cruiser1_Sink3.png")).convert_alpha()
cruiser1_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser1\Cruiser1_Sink4.png")).convert_alpha()
cruiser1_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser1\Cruiser1_Sink5.png")).convert_alpha()

cruiser2_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser2\Cruiser2_Sink1.png")).convert_alpha()
cruiser2_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser2\Cruiser2_Sink2.png")).convert_alpha()
cruiser2_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser2\Cruiser2_Sink3.png")).convert_alpha()
cruiser2_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser2\Cruiser2_Sink4.png")).convert_alpha()
cruiser2_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser2\Cruiser2_Sink5.png")).convert_alpha()

cruiser3_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser3\Cruiser3_Sink1.png")).convert_alpha()
cruiser3_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser3\Cruiser3_Sink2.png")).convert_alpha()
cruiser3_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser3\Cruiser3_Sink3.png")).convert_alpha()
cruiser3_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser3\Cruiser3_Sink4.png")).convert_alpha()
cruiser3_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims\Cruiser\Cruiser3\Cruiser3_Sink5.png")).convert_alpha()


battleship1_tile = pygame.image.load(resource_path("images\isometric tiles/bttlship1.png")).convert_alpha()
battleship2_tile = pygame.image.load(resource_path("images\isometric tiles/bttlship2.png")).convert_alpha()
battleship3_tile = pygame.image.load(resource_path("images\isometric tiles/bttlship3.png")).convert_alpha()
battleship4_tile = pygame.image.load(resource_path("images\isometric tiles/bttlship4.png")).convert_alpha()
battleshipC_tile = pygame.image.load(resource_path("images\isometric tiles/bttlshipC.png")).convert_alpha()
battleshipX_tile = pygame.image.load(resource_path("images\isometric tiles/bttlshipX.png")).convert_alpha()

battleship1_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship1/battleship1_Sink1.png")).convert_alpha()
battleship1_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship1/battleship1_Sink2.png")).convert_alpha()
battleship1_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship1/battleship1_Sink3.png")).convert_alpha()
battleship1_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship1/battleship1_Sink4.png")).convert_alpha()
battleship1_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship1/battleship1_Sink5.png")).convert_alpha()

battleship2_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship2/battleship2_Sink1.png")).convert_alpha()
battleship2_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship2/battleship2_Sink2.png")).convert_alpha()
battleship2_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship2/battleship2_Sink3.png")).convert_alpha()
battleship2_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship2/battleship2_Sink4.png")).convert_alpha()
battleship2_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship2/battleship2_Sink5.png")).convert_alpha()

battleship3_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship3/battleship3_Sink1.png")).convert_alpha()
battleship3_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship3/battleship3_Sink2.png")).convert_alpha()
battleship3_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship3/battleship3_Sink3.png")).convert_alpha()
battleship3_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship3/battleship3_Sink4.png")).convert_alpha()
battleship3_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship3/battleship3_Sink5.png")).convert_alpha()

battleship4_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship4/battleship4_Sink1.png")).convert_alpha()
battleship4_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship4/battleship4_Sink2.png")).convert_alpha()
battleship4_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship4/battleship4_Sink3.png")).convert_alpha()
battleship4_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship4/battleship4_Sink4.png")).convert_alpha()
battleship4_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/battleship/battleship4/battleship4_Sink5.png")).convert_alpha()


carrier1_tile = pygame.image.load(resource_path("images\isometric tiles\carrier1.png")).convert_alpha()
carrier2_tile = pygame.image.load(resource_path("images\isometric tiles\carrier2.png")).convert_alpha()
carrier3_tile = pygame.image.load(resource_path("images\isometric tiles\carrier3.png")).convert_alpha()
carrier4_tile = pygame.image.load(resource_path("images\isometric tiles\carrier2.png")).convert_alpha()
carrier5_tile = pygame.image.load(resource_path("images\isometric tiles\carrier4.png")).convert_alpha()
carrierC_tile = pygame.image.load(resource_path("images\isometric tiles\carrierC.png")).convert_alpha()
carrierX_tile = pygame.image.load(resource_path("images\isometric tiles\carrierX.png")).convert_alpha()

carrier1_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier1/carrier1_Sink1.png")).convert_alpha()
carrier1_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier1/carrier1_Sink2.png")).convert_alpha()
carrier1_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier1/carrier1_Sink3.png")).convert_alpha()
carrier1_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier1/carrier1_Sink4.png")).convert_alpha()
carrier1_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier1/carrier1_Sink5.png")).convert_alpha()

carrier2_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier2/carrier2_Sink1.png")).convert_alpha()
carrier2_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier2/carrier2_Sink2.png")).convert_alpha()
carrier2_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier2/carrier2_Sink3.png")).convert_alpha()
carrier2_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier2/carrier2_Sink4.png")).convert_alpha()
carrier2_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier2/carrier2_Sink5.png")).convert_alpha()

carrier3_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier3/carrier3_Sink1.png")).convert_alpha()
carrier3_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier3/carrier3_Sink2.png")).convert_alpha()
carrier3_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier3/carrier3_Sink3.png")).convert_alpha()
carrier3_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier3/carrier3_Sink4.png")).convert_alpha()
carrier3_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier3/carrier3_Sink5.png")).convert_alpha()

carrier4_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier4/carrier4_Sink1.png")).convert_alpha()
carrier4_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier4/carrier4_Sink2.png")).convert_alpha()
carrier4_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier4/carrier4_Sink3.png")).convert_alpha()
carrier4_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier4/carrier4_Sink4.png")).convert_alpha()
carrier4_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier4/carrier4_Sink5.png")).convert_alpha()

carrier5_sink1 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier5/carrier5_Sink1.png")).convert_alpha()
carrier5_sink2 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier5/carrier5_Sink2.png")).convert_alpha()
carrier5_sink3 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier5/carrier5_Sink3.png")).convert_alpha()
carrier5_sink4 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier5/carrier5_Sink4.png")).convert_alpha()
carrier5_sink5 = pygame.image.load(resource_path("images\isometric tiles\Sink Anims/carrier/carrier5/carrier5_Sink5.png")).convert_alpha()



game_screen = "main"

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

startup_ticks = 0

selectedPlayerMode = True
difficulty = "Easy"
dbltime = 1 #used for dev bugtesting, anims play at double time when set to 2.
# this however breaks sounds. setting to any other value other than 1 or 2 may break the game completely
devmode = 1 #used for dev bugtesting, mostly used for viewing ship grids, 1 to enable, 0 to disable
unfairness_multiplier = 0 #number form 0-10, increases chance that the AI will automatically target a ship, used to speed up games

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
target_cell = pygame.Vector2(0,0)
left_size = 0
right_size = 0
left_pos = pygame.Vector2(0, 0)
right_pos = pygame.Vector2(0, 0)

AI_hit_reg = []
Prev_action = []
locked_on_ship = False
lock_coords = pygame.Vector2(0, 0)
check_dir = 0
found_dir = 0
double_check = 0

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
carrier: dict = {0: carrier5_tile,
                    1: carrier4_tile,
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

# main widgets
playGame = widgets.Button(640, 250, playButton_img, 3, playButton_hover)
optionsButton = widgets.Button(640, 375, optionButton_img, 3, optionButton_hover)
openCredits = widgets.Button(640, 500, creditsButton_img, 3, creditsButton_hover)
exitGame = widgets.Button(640, 625, exitButton_img, 3, exitButton_hover)
black = widgets.Image(0, 0, black_screen, 4)

# option widgets
backButton = widgets.Button(75, 75, backButton_img, 2)
masterVolume = slider.Slider(300, 200, 500, master_lvl)
musicVolume = slider.Slider(300, 300, 500, music_lvl)
sfxVolume = slider.Slider(300, 400, 500, sfx_lvl)

# game options widgets
selectPlayer = widgets.Toggle(640, 300, select1P_img, select2P_img, 1.2)
selectDiff = widgets.Toggle(640, 430, selectDiffEasy_img, selectDiffHard_img, 0.7)
gameOptionsProceed = widgets.Button(640, 570, playButton_img, 3, playButton_hover)

player1Board = widgets.Image(200, 360, player1Board_img, 1)
player2Board = widgets.Image(1080, 360, player2Board_img, 1)
aiEasyBoard = widgets.Image(1080, 360, ai_easy_Board_img, 1)
aiHardBoard = widgets.Image(1080, 360, ai_hard_Board_img, 1)
middleBoard = widgets.Image(640, 360, middle_Board_img, 1)

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

scroll = 0
running = True
while running:

    screen.fill((110, 110, 110))
    placementSurface.fill((0, 0, 0, 0))
    hud.fill((0, 0, 0, 0))
    leftRender.fill((0, 0, 0, 0))
    leftOverlay.fill((0, 0, 0, 0))
    rightRender.fill((0, 0, 0, 0))
    rightOverlay.fill((0, 0, 0, 0))
    # leftOverlay.fill((0, 0, 0, 0))
    # leftRender.fill((176, 11, 19, 150)) #blue
    # rightOverlay.fill((106, 227, 82, 150)) #red
    # rightRender.fill((42, 6, 90, 150)) #green

    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    if game_screen == "main":
        scale = 1
        bg_tile = math.ceil(SCREEN_WIDTH/(1280*scale))+1
        if startup_ticks in range(0, 240):
            screen.blit(pygame.transform.scale(ocean_screen, (1280*scale, 720*scale)), (0, 0))
        else:
            for i in range(0, bg_tile):
                screen.blit(pygame.transform.scale(ocean_screen, (1280*scale, 720*scale)), (i * 1280*scale + scroll, 0))
        
        scroll -= 1

        if abs(scroll) > 1280:
            scroll = 0

        delay = 75
        if startup_ticks in range(0, delay+30):
            f = 2
            if (startup_ticks-delay) // f <= f*0:
                startup_door = widgets.Image(640, 360, blast_door_1, 1)
            elif (startup_ticks-delay) // f == f*1:
                startup_door = widgets.Image(640, 360, blast_door_2, 1)
            elif (startup_ticks-delay) // f == f*2:
                startup_door = widgets.Image(640, 360, blast_door_3, 1)
            elif (startup_ticks-delay) // f == f*3:
                startup_door = widgets.Image(640, 360, blast_door_4, 1)
            elif (startup_ticks-delay) // f == f*4:
                startup_door = widgets.Image(640, 360, blast_door_5, 1)
            elif (startup_ticks-delay) // f == f*5:
                startup_door = widgets.Image(640, 360, blast_door_6, 1)
            elif (startup_ticks-delay) // f == f*6:
                startup_door = widgets.Image(640, 360, blast_door_7, 1)
            elif (startup_ticks-delay) // f == f*7:
                startup_door = widgets.Image(640, 360, blast_door_8, 1)
            
            startup_door.draw(screen)
        
        if startup_ticks <= 100:
            black.draw(screen, 250-2.5*startup_ticks)

        if startup_ticks == 1:
            # pygame.mixer.Sound.play(startup_jingle)
            pygame.mixer.music.play()

        delay = 200
        duration = 40
        if delay < startup_ticks < delay+duration:
            font2 = pygame.font.Font(resource_path("fonts\Crang.ttf"), (84+((delay+duration-startup_ticks)*6)))
        elif startup_ticks == delay+duration:
            font2 = pygame.font.Font(resource_path("fonts\Crang.ttf"), 84)
            pygame.mixer.Sound.play(startup_sfx1)
        elif startup_ticks > delay+duration:
            font2 = pygame.font.Font(resource_path("fonts\Crang.ttf"), 84)
        
        if startup_ticks > delay:
            draw_text("Battleships", font2, (0, 0, 0), (1280-font2.size("Battleships")[0])/2, 50)
        
        

        pause = 14
        interval = 10
        if startup_ticks == delay+pause+duration+interval:
            pygame.mixer.Sound.play(startup_sfx2)
        if startup_ticks >= delay+pause+duration+interval:
             if playGame.draw(screen):
                 switch("game options")
        
        if startup_ticks == delay+pause+duration+interval*2:
            pygame.mixer.Sound.play(startup_sfx2)
        if startup_ticks >= delay+pause+duration+interval*2:
            if optionsButton.draw(screen):
                switch("options")

        if startup_ticks == delay+pause+duration+interval*3:
            pygame.mixer.Sound.play(startup_sfx2)
        if startup_ticks >= delay+pause+duration+interval*3:
            if openCredits.draw(screen):
                switch("credits")

        if startup_ticks == delay+pause+duration+interval*4:
            pygame.mixer.Sound.play(startup_sfx2)
        if startup_ticks >= delay+pause+duration+interval*4:
            if exitGame.draw(screen):
                if messagebox.askokcancel("Close Game?", "You are about to leave the game. Continue?"):
                    running = False

        startup_ticks += 1

    elif game_screen == "options":
        screen.blit(pygame.transform.scale(ocean_screen, (1280*scale, 720*scale)), (0, 0))
        screen.blit(big_Board_img, (0, 0))

        if backButton.draw(hud):
            switch("main")

        master_lvl = masterVolume.draw(hud)

        sfx_lvl = sfxVolume.draw(hud)
        startup_sfx1.set_volume(sfx_lvl*master_lvl)
        startup_sfx2.set_volume(sfx_lvl*master_lvl)
        place_sfx1.set_volume(sfx_lvl*master_lvl)
        denyClick_sfx1.set_volume(sfx_lvl*master_lvl)
        explosion_sfx1.set_volume(sfx_lvl*master_lvl)
        explosion_sfx2.set_volume(sfx_lvl*master_lvl)
        explosion_sfx3.set_volume(sfx_lvl*master_lvl)
        explosion_sfx4.set_volume(sfx_lvl*master_lvl)
        splash_sfx1.set_volume(sfx_lvl*master_lvl)
        splash_sfx2.set_volume(sfx_lvl*master_lvl)
        splash_sfx3.set_volume(sfx_lvl*master_lvl)
        splash_sfx4.set_volume(sfx_lvl*master_lvl)
        splash_sfx5.set_volume(sfx_lvl*master_lvl)

        music_lvl = musicVolume.draw(hud)
        pygame.mixer.music.set_volume(music_lvl*master_lvl)

    elif game_screen == "credits":
        if backButton.draw(hud):
            switch("main")

    elif game_screen == "game options":
        middleBoard.draw(hud)

        draw_text("Game Options", font1, (0, 0, 0), (1280-font1.size("Game Options")[0])/2, 100)
        selectedPlayerMode = selectPlayer.draw(hud, output=0)
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
        if gameOptionsProceed.draw(hud):
            winner = "undecided"
            switch("page router")
    
    elif game_screen == "page router":
        if inGame == False: #if not in game i.e. setting up new game
            #reset vars for boat placement screens
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
            # reset vars for prompt screens
            prompt_cd = 60
            if selectedPlayerMode == False: #if 1 player mode was selected
                if playersReady == 0: #if no players have placed boats i.e if the player is about to place boats
                    playersReady = 1
                    switch("P1Prompt")
                elif playersReady == 1: #if the player has placed boats i.e AI is ready to prepare for game
                    P1Boats = PlacingGrid
                    P1Rot = BoatRotation
                    playersReady = 2
                    switch("AIPrep")
            else: #if 2 player mode was selected
                if playersReady == 0: #if no players have placed boats i.e if player 1 is about to place boats
                    playersReady = 1
                    switch("P1Prompt")
                elif playersReady == 1: #if only 1 player has placed boats i.e if player 2 is about to place boats
                    P1Boats = PlacingGrid
                    P1Rot = BoatRotation
                    playersReady = 2
                    switch("P2Prompt")
                elif playersReady == 2: #if both players have placed boats
                    P2Boats = PlacingGrid
                    P2Rot = BoatRotation
                    playersReady = 3
                    switch("GameReady")
            BoatRotation = [0, 0, 0, 0, 0]
            PlacingGrid = copy.deepcopy(BlankGrid)
        else: #if currently in game
            if turn != 0:
                if P1Boats_sunk == [1, 1, 1, 1, 1]:
                    winner = "Player 2"
                if P2Boats_sunk == [1, 1, 1, 1, 1]:
                    winner = "Player 1"

            turn += 1 #on init turn is 0, first turn changes to 1
            selected_cell = pygame.Vector2(0,0)
            mov_cd = 0
            nuke_anim = False
            nuke_anim2 = False
            nuke_ticks = 0
            if winner == "undecided":
                if turn == 1: #on first turn
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    anim_ticks = 0
                    destroyer_sink_anim = False
                    submarine_sink_anim = False
                    cruiser_sink_anim = False
                    battleship_sink_anim = False
                    carrier_sink_anim = False
                    sink_anim_ticks = 0
                    P1Boats_sunk = [0, 0, 0, 0, 0]
                    P2Boats_sunk = [0, 0, 0, 0, 0]
                    x = 0
                    y = 0
                    target_cell = pygame.Vector2(0,0)
                    locked_on_ship = False
                    uncleared_cells = []
                    switch("P1Game")
                    door_anim = False
                    door_ticks = 0
                else:
                    if selectedPlayerMode == False: # one player mode
                        if turn % 2 == 1:
                            anim_ticks = 0
                            switch("P1Game")
                        else:
                            anim_ticks = 0
                            switch("AI Turn")
                    else:
                        if turn % 2 == 1:
                            pass
                        else:
                            pass
            else: #if someone has won the game
                door_ticks = 0
                door_anim = True
                switch("win")
    
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
                                if PlacingGrid[j][i] in [10, 11]:
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
                                if PlacingGrid[j][i] in [20, 21, 22]:
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
                                if PlacingGrid[j][i] in [30, 31, 32]:
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
                                if PlacingGrid[j][i] in [40, 41, 42, 43]:
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
                                if PlacingGrid[j][i] in [50, 51, 52, 53, 54]:
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
                                if PlacingGrid[j][i] in [10, 11]:
                                    PlacingGrid[j][i] = 00
                            if selected_boat == 1:
                                if PlacingGrid[j][i] in [20, 21, 22]:
                                    PlacingGrid[j][i] = 00
                            if selected_boat == 2:
                                if PlacingGrid[j][i] in [30, 31, 32]:
                                    PlacingGrid[j][i] = 00
                            if selected_boat == 3:
                                if PlacingGrid[j][i] == [40, 41, 42, 43]:
                                    PlacingGrid[j][i] = 00
                            if selected_boat == 4:
                                if PlacingGrid[j][i] == [50, 51, 52, 53, 54]:
                                    PlacingGrid[j][i] = 00
                            if selected_boat == 5:
                                pass
                    if selected_boat != 5:
                        StoredBoats[selected_boat] = 1
                        selected_boat = 5
                        selected_cell = pygame.Vector2(10, 10)
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
                            50: carrier5_tile,
                            51: carrier4_tile,
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
                            carrier5_tile: 50,
                            carrier4_tile: 51,
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
                if tile in [10, 11]:
                    boat_type = 0
                if tile in [20, 21, 22]:
                    boat_type = 1
                if tile in [30, 31, 32]:
                    boat_type = 2
                if tile in [40, 41, 42, 43]:
                    boat_type = 3
                if tile in [50, 51, 52, 53, 54]:
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
        stamp_cd -= 1
        store_cd -= 1

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
            switch("page router")

    elif game_screen == "AI Turn":
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
                            50: carrier5_tile,
                            51: carrier4_tile,
                            52: carrier3_tile,
                            53: carrier2_tile,
                            54: carrier1_tile,
                            99: "blank"
                            }

        mov_cd -= 1

        # left render
        for y, row in enumerate(P2Boats):
            for x, tile in enumerate(row):
                xdil = 16
                ydil = 8
                boat_type = 9  
                rotate_cell = None              
                if tile in range(10, 20):
                    boat_type = 0
                if tile in range(20, 30):
                    boat_type = 1
                if tile in range(30, 40):
                    boat_type = 2
                if tile in range(40, 50):
                    boat_type = 3
                if tile in range(50, 60):
                    boat_type = 4
                
                if boat_type != 9:
                    if P2Rot[boat_type] == 0:
                        rotate_cell = False
                    elif P2Rot[boat_type] == 1:
                        rotate_cell = True

                if tile in [10, 11, 20, 21, 22, 30, 31, 32, 40, 41, 42, 43, 50, 51, 52, 53, 54] and not keys[pygame.K_f]:
                    tile_sprite = d_sea_tile
                elif tile == 5:
                    tile_sprite = d_sea_nohit_tile
                elif tile in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    tile_sprite = d_sea_hit_tile
                    hit_tiles = {
                        15: destroyer2_sink5,
                        16: destroyer1_sink5,
                        25: submarine3_sink5,
                        26: submarine2_sink5,
                        27: submarine1_sink5,
                        35: cruiser3_sink5,
                        36: cruiser2_sink5,
                        37: cruiser1_sink5,
                        45: battleship4_sink5,
                        46: battleship3_sink5,
                        47: battleship2_sink5,
                        48: battleship1_sink5,
                        55: carrier5_sink5,
                        56: carrier4_sink5,
                        57: carrier3_sink5,
                        58: carrier2_sink5,
                        59: carrier1_sink5
                    }
                    if (P2Boats_sunk[0] == 1 and tile in [15, 16]) or (P2Boats_sunk[1] == 1 and tile in [25, 26, 27])\
                        or (P2Boats_sunk[2] == 1 and tile in [35, 36, 37]) or (P2Boats_sunk[3] == 1 and tile in [45, 46, 47, 48])\
                        or (P2Boats_sunk[4] == 1 and tile in [55, 56, 57, 58, 59]):
                        tile_sprite = hit_tiles.get(tile, d_sea_hit_tile)
                else:
                    tile_sprite = funcs.get(tile, "blank")
                        
                if tile_sprite == "blank":
                    pass
                elif rotate_cell == False:
                    leftRender.blit(tile_sprite, (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
                else:
                    leftRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))

        # right render
        for y, row in enumerate(P1Boats):
            for x, tile in enumerate(row):
                xdil = 16
                ydil = 8
                boat_type = 9  
                rotate_cell = None              
                if tile in range(10, 20):
                    boat_type = 0
                if tile in range(20, 30):
                    boat_type = 1
                if tile in range(30, 40):
                    boat_type = 2
                if tile in range(40, 50):
                    boat_type = 3
                if tile in range(50, 60):
                    boat_type = 4
                
                if boat_type != 9:
                    if P1Rot[boat_type] == 0:
                        rotate_cell = False
                    elif P1Rot[boat_type] == 1:
                        rotate_cell = True
                
                if tile == 5:
                    tile_sprite = d_sea_nohit_tile
                elif tile in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    tile_sprite = d_sea_hit_tile
                    hit_tiles = {
                        15: destroyer2_sink5,
                        16: destroyer1_sink5,
                        25: submarine3_sink5,
                        26: submarine2_sink5,
                        27: submarine1_sink5,
                        35: cruiser3_sink5,
                        36: cruiser2_sink5,
                        37: cruiser1_sink5,
                        45: battleship4_sink5,
                        46: battleship3_sink5,
                        47: battleship2_sink5,
                        48: battleship1_sink5,
                        55: carrier5_sink5,
                        56: carrier4_sink5,
                        57: carrier3_sink5,
                        58: carrier2_sink5,
                        59: carrier1_sink5
                    }
                    if (P1Boats_sunk[0] == 1 and tile in [15, 16]) or (P1Boats_sunk[1] == 1 and tile in [25, 26, 27])\
                        or (P1Boats_sunk[2] == 1 and tile in [35, 36, 37]) or (P1Boats_sunk[3] == 1 and tile in [45, 46, 47, 48])\
                        or (P1Boats_sunk[4] == 1 and tile in [55, 56, 57, 58, 59]):
                        tile_sprite = hit_tiles.get(tile, d_sea_hit_tile)
                else:
                    tile_sprite = funcs.get(tile, "blank")

                if tile_sprite == "blank":
                    pass
                elif rotate_cell == False:
                    rightRender.blit(tile_sprite, (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
                else:
                    rightRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))


        keys = pygame.key.get_pressed()

        if keys[pygame.K_e]:
            anim_ticks = 0

        t = 30
        scale = 10
        diff = 1.5
        delay = 90
        if anim_ticks <= delay:
            left_size = screen.get_width()/2 + scale*(1 + (0.5*t)*diff)
            right_size = screen.get_width()/2 + scale*(1 - (0.5*t)*diff)
            left_pos = pygame.Vector2(55, 50-(left_size*0.13))
            right_pos = pygame.Vector2(1225-right_size, 670-(right_size*0.69))
            anim_ticks += 1*dbltime
        elif delay < anim_ticks <= delay + t:
            left_size = screen.get_width()/2 + scale*(1 + (0.5*t - (anim_ticks - delay))*diff)
            right_size = screen.get_width()/2 + scale*(1 - (0.5*t - (anim_ticks - delay))*diff)
            left_pos = pygame.Vector2(55, 50-(left_size*0.13))
            right_pos = pygame.Vector2(1225-right_size, 670-(right_size*0.69))
            anim_ticks += 1*dbltime
        else:
            if difficulty == "Easy":
                while True:
                    decision = random.randint(0, 99)
                    if decision in AI_hit_reg:
                        pass
                    else:
                        AI_hit_reg.append(decision)
                        x = int(decision % 10)
                        y = int((decision - x) / 10)
                        P1Boats[y][x] += 5
                        Prev_action.append(decision)
                        if P1Boats[y][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                            pass
                        else:
                            switch("page router")
                            break
            elif difficulty == "Hard":
                if locked_on_ship == False:
                    while True:
                        if len(uncleared_cells) > 0:
                            locked_on_ship = True
                            lock_coords = pygame.Vector2(uncleared_cells[0]%10, (uncleared_cells[0]-(uncleared_cells[0]%10))/10)
                            OG_coords = pygame.Vector2(uncleared_cells[0]%10, (uncleared_cells[0]-(uncleared_cells[0]%10))/10)
                            check_dir = 1
                            found_dir = 0
                            double_check = 0
                            break

                        if unfairness_multiplier > random.randint(0, 9):
                            decision = random.randint(0, 99)
                            if decision in AI_hit_reg:
                                pass
                            else:
                                x = int(decision % 10)
                                y = int((decision - x) / 10)
                                if P1Boats[y][x] in [10, 11, 20, 21, 22, 30, 31, 32, 40, 41, 42, 43, 50, 51, 52, 53, 54]:
                                    AI_hit_reg.append(decision)
                                    P1Boats[y][x] += 5
                                    Prev_action.append(decision)
                                    locked_on_ship = True
                                    lock_coords = pygame.Vector2(x, y)
                                    OG_coords = pygame.Vector2(x, y)
                                    check_dir = 1
                                    found_dir = 0
                                    double_check = 0
                                    uncleared_cells = [10*y+x]
                                    break
                        else:
                            offset = random.randint(0, 1)
                            row = random.randint(0, 4)
                            column = random.randint(0, 4)

                            true_row = 2*row + offset
                            true_column = 2*column + offset
                            true_loc = true_row*10+true_column
                            if true_loc in AI_hit_reg:
                                pass
                            else:
                                AI_hit_reg.append(true_loc)
                                x = true_column
                                y = true_row
                                P1Boats[y][x] += 5
                                Prev_action.append(10*y+x)
                                if P1Boats[y][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    locked_on_ship = True
                                    lock_coords = pygame.Vector2(x, y)
                                    OG_coords = pygame.Vector2(x, y)
                                    check_dir = 1
                                    found_dir = 0
                                    double_check = 0
                                    uncleared_cells = [10*y+x]
                                    break
                                else:
                                    switch("page router")
                                    break
                if locked_on_ship == True:
                    x = int(lock_coords.x)
                    y = int(lock_coords.y)
                    if found_dir == 0:
                        while True:
                            if check_dir == 1:
                                if y == 0 or P1Boats[y-1][x] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    check_dir = 2
                                    lock_coords = OG_coords
                                elif not 10*(y-1)+x in AI_hit_reg:
                                    AI_hit_reg.append(10*(y-1)+x)
                                    P1Boats[y-1][x] += 5
                                    Prev_action.append(10*(y-1)+x)
                                    if P1Boats[y-1][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                        found_dir = 1
                                        uncleared_cells.append(10*(y-1)+x)
                                        lock_coords = pygame.Vector2(x, y-1)
                                        break
                                    else:
                                        check_dir = 2
                                        lock_coords = OG_coords
                                        switch("page router")
                                        break
                                else:
                                    check_dir = 2
                                    lock_coords = OG_coords
                            elif check_dir == 2:
                                if x == 9 or P1Boats[y][x+1] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    check_dir = 3
                                    lock_coords = OG_coords
                                elif not 10*y+(x+1) in AI_hit_reg:
                                    AI_hit_reg.append(10*y+(x+1))
                                    P1Boats[y][x+1] += 5
                                    Prev_action.append(10*y+(x+1))
                                    if P1Boats[y][x+1] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                        found_dir = 2
                                        uncleared_cells.append(10*y+(x+1))
                                        lock_coords = pygame.Vector2(x+1, y)
                                        break
                                    else:
                                        check_dir = 3
                                        lock_coords = OG_coords
                                        switch("page router")
                                        break
                                else:
                                    check_dir = 3
                                    lock_coords = OG_coords
                            elif check_dir == 3:
                                if y == 9 or P1Boats[y+1][x] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    check_dir = 4
                                    lock_coords = OG_coords
                                elif not 10*(y+1)+x in AI_hit_reg:
                                    AI_hit_reg.append(10*(y+1)+x)
                                    P1Boats[y+1][x] += 5
                                    Prev_action.append(10*(y+1)+x)
                                    if P1Boats[y+1][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                        found_dir = 3
                                        uncleared_cells.append(10*(y+1)+x)
                                        lock_coords = pygame.Vector2(x, y+1)
                                        break
                                    else:
                                        check_dir = 4
                                        lock_coords = OG_coords
                                        switch("page router")
                                        break
                                else:
                                    check_dir = 4
                                    lock_coords = OG_coords
                            elif check_dir == 4:
                                if x == 0 or P1Boats[y][x-1] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    locked_on_ship = False
                                    uncleared_cells.pop(0)
                                    break
                                elif not 10*y+(x-1) in AI_hit_reg:
                                    AI_hit_reg.append(10*y+(x-1))
                                    P1Boats[y][x-1] += 5
                                    Prev_action.append(10*y+(x-1))
                                    if P1Boats[y][x-1] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                        found_dir = 4
                                        uncleared_cells.append(10*y+(x-1))
                                        lock_coords = pygame.Vector2(x-1, y)
                                        break
                                    else:
                                        locked_on_ship = False
                                        switch("page router")
                                        break
                    else:
                        lock = True
                        while lock:
                            x = int(lock_coords.x)
                            y = int(lock_coords.y)
                            if found_dir == 1:
                                if y == 0 or P1Boats[y-1][x] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    found_dir = 3
                                    lock_coords = OG_coords
                                    double_check += 1
                                else:
                                    AI_hit_reg.append(10*(y-1)+x)
                                    P1Boats[y-1][x] += 5
                                    Prev_action.append(10*(y-1)+x)
                                    if P1Boats[y-1][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                        lock_coords = pygame.Vector2(x, y-1)
                                        uncleared_cells.append(10*(y-1)+x)
                                    else:
                                        found_dir = 3
                                        lock_coords = OG_coords
                                        double_check += 1
                                        switch("page router")
                                        lock = False
                            elif found_dir == 2:
                                if x == 9 or P1Boats[y][x+1] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    found_dir = 4
                                    lock_coords = OG_coords
                                    double_check += 1
                                else:
                                    AI_hit_reg.append(10*y+(x+1))
                                    P1Boats[y][x+1] += 5
                                    Prev_action.append(10*y+(x+1))
                                    if P1Boats[y][x+1] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                        lock_coords = pygame.Vector2(x+1, y)
                                        uncleared_cells.append(10*y+(x+1))
                                    else:
                                        found_dir = 4
                                        lock_coords = OG_coords
                                        double_check += 1
                                        switch("page router")
                                        lock = False
                            elif found_dir == 3:
                                if y == 9 or P1Boats[y+1][x] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    found_dir = 1
                                    lock_coords = OG_coords
                                    double_check += 1
                                else:
                                    AI_hit_reg.append(10*(y+1)+x)
                                    P1Boats[y+1][x] += 5
                                    Prev_action.append(10*(y+1)+x)
                                    if P1Boats[y+1][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                        lock_coords = pygame.Vector2(x, y+1)
                                        uncleared_cells.append(10*(y+1)+x)
                                    else:
                                        found_dir = 1
                                        lock_coords = OG_coords
                                        double_check += 1
                                        switch("page router")
                                        lock = False
                            elif found_dir == 4:
                                if x == 0 or P1Boats[y][x-1] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    found_dir = 2
                                    lock_coords = OG_coords
                                    double_check += 1
                                else:
                                    AI_hit_reg.append(10*y+(x-1))
                                    P1Boats[y][x-1] += 5
                                    Prev_action.append(10*y+(x-1))
                                    if P1Boats[y][x-1] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                        lock_coords = pygame.Vector2(x-1, y)
                                        uncleared_cells.append(10*y+(x-1))
                                    else:
                                        found_dir = 2
                                        lock_coords = OG_coords
                                        double_check += 1
                                        switch("page router")
                                        lock = False
                            if any(15 in sl for sl in P1Boats) and any(16 in sl for sl in P1Boats) and P1Boats_sunk[0] == 0:
                                locked_on_ship = False
                                double_check -= 1
                                P1Boats_sunk[0] = 1
                                print("sunk destroyer")
                                lock = False
                            elif any(25 in sl for sl in P1Boats) and any(26 in sl for sl in P1Boats) and any(27 in sl for sl in P1Boats) and P1Boats_sunk[1] == 0:
                                locked_on_ship = False
                                double_check -= 1
                                P1Boats_sunk[1] = 1
                                print("sunk submarine")
                                lock = False
                            elif any(35 in sl for sl in P1Boats) and any(36 in sl for sl in P1Boats) and any(37 in sl for sl in P1Boats) and P1Boats_sunk[2] == 0:
                                locked_on_ship = False
                                double_check -= 1
                                P1Boats_sunk[2] = 1
                                print("sunk cruiser")
                                lock = False
                            elif any(45 in sl for sl in P1Boats) and any(46 in sl for sl in P1Boats) and any(47 in sl for sl in P1Boats) and any(48 in sl for sl in P1Boats) and P1Boats_sunk[3] == 0:
                                locked_on_ship = False
                                double_check -= 1
                                P1Boats_sunk[3] = 1
                                print("sunk battleship")
                                lock = False
                            elif any(55 in sl for sl in P1Boats) and any(56 in sl for sl in P1Boats) and any(57 in sl for sl in P1Boats) and any(58 in sl for sl in P1Boats) and any(59 in sl for sl in P1Boats) and P1Boats_sunk[4] == 0:
                                locked_on_ship = False
                                double_check -= 1
                                P1Boats_sunk[4] = 1
                                print("sunk carrier")
                                lock = False
                            for i in uncleared_cells:
                                cell = P1Boats[int((i-(i%10))/10)][int(i%10)]
                                if (cell in [15, 16] and P1Boats_sunk[0] == 1)\
                                     or (cell in [25, 26, 27] and P1Boats_sunk[1] == 1)\
                                     or (cell in [35, 36, 37] and P1Boats_sunk[2] == 1)\
                                     or (cell in [45, 46, 47, 48] and P1Boats_sunk[3] == 1)\
                                     or (cell in [55, 56, 57, 58, 59] and P1Boats_sunk[4] == 1):
                                    uncleared_cells.remove(i)
                            if double_check == 2:
                                locked_on_ship = False
                                double_check = 0
                                lock = False

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
                            50: carrier5_tile,
                            51: carrier4_tile,
                            52: carrier3_tile,
                            53: carrier2_tile,
                            54: carrier1_tile,
                            99: "blank"
                            }
        
        if mov_cd <= 0 and nuke_anim == False and destroyer_sink_anim == False and submarine_sink_anim == False\
            and cruiser_sink_anim == False and battleship_sink_anim == False and carrier_sink_anim == False:
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

        mov_cd -= 1

        # left render
        for y, row in enumerate(P2Boats):
            for x, tile in enumerate(row):
                xdil = 16
                ydil = 8
                boat_type = 9  
                rotate_cell = None              
                if tile in range(10, 20):
                    boat_type = 0
                if tile in range(20, 30):
                    boat_type = 1
                if tile in range(30, 40):
                    boat_type = 2
                if tile in range(40, 50):
                    boat_type = 3
                if tile in range(50, 60):
                    boat_type = 4
                
                if boat_type != 9:
                    if P2Rot[boat_type] == 0:
                        rotate_cell = False
                    elif P2Rot[boat_type] == 1:
                        rotate_cell = True

                if tile in [10, 11, 20, 21, 22, 30, 31, 32, 40, 41, 42, 43, 50, 51, 52, 53, 54] and not (devmode == 1 and keys[pygame.K_f]):
                    tile_sprite = d_sea_tile
                elif tile == 5:
                    tile_sprite = d_sea_nohit_tile
                elif tile in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    tile_sprite = d_sea_hit_tile
                    hit_tiles = {
                        15: destroyer2_sink5,
                        16: destroyer1_sink5,
                        25: submarine3_sink5,
                        26: submarine2_sink5,
                        27: submarine1_sink5,
                        35: cruiser3_sink5,
                        36: cruiser2_sink5,
                        37: cruiser1_sink5,
                        45: battleship4_sink5,
                        46: battleship3_sink5,
                        47: battleship2_sink5,
                        48: battleship1_sink5,
                        55: carrier5_sink5,
                        56: carrier4_sink5,
                        57: carrier3_sink5,
                        58: carrier2_sink5,
                        59: carrier1_sink5
                    }
                    if (P2Boats_sunk[0] == 1 and tile in [15, 16]) or (P2Boats_sunk[1] == 1 and tile in [25, 26, 27])\
                        or (P2Boats_sunk[2] == 1 and tile in [35, 36, 37]) or (P2Boats_sunk[3] == 1 and tile in [45, 46, 47, 48])\
                        or (P2Boats_sunk[4] == 1 and tile in [55, 56, 57, 58, 59]):
                        tile_sprite = hit_tiles.get(tile, d_sea_hit_tile)
                else:
                    tile_sprite = funcs.get(tile, "blank")

                if destroyer_sink_anim == True:
                    if sink_anim_ticks in range(0, 15):
                        if tile == 15:
                            tile_sprite = destroyer2_sink1
                        elif tile == 16:
                            tile_sprite = destroyer1_sink1
                    elif sink_anim_ticks in range(15, 30):
                        if tile == 15:
                            tile_sprite = destroyer2_sink2
                        elif tile == 16:
                            tile_sprite = destroyer1_sink2
                    elif sink_anim_ticks in range(30, 45):
                        if tile == 15:
                            tile_sprite = destroyer2_sink3
                        elif tile == 16:
                            tile_sprite = destroyer1_sink3
                    elif sink_anim_ticks in range(45, 60):
                        if tile == 15:
                            tile_sprite = destroyer2_sink4
                        elif tile == 16:
                            tile_sprite = destroyer1_sink4
                    elif sink_anim_ticks in range(60, 75):
                        if tile == 15:
                            tile_sprite = destroyer2_sink5
                        elif tile == 16:
                            tile_sprite = destroyer1_sink5

                if submarine_sink_anim == True:
                    if sink_anim_ticks in range(0, 15):
                        if tile == 25:
                            tile_sprite = submarine3_sink1
                        elif tile == 26:
                            tile_sprite = submarine2_sink1
                        elif tile == 27:
                            tile_sprite = submarine1_sink1
                    elif sink_anim_ticks in range(15, 30):
                        if tile == 25:
                            tile_sprite = submarine3_sink2
                        elif tile == 26:
                            tile_sprite = submarine2_sink2
                        elif tile == 27:
                            tile_sprite = submarine1_sink2
                    elif sink_anim_ticks in range(30, 45):
                        if tile == 25:
                            tile_sprite = submarine3_sink3
                        elif tile == 26:
                            tile_sprite = submarine2_sink3
                        elif tile == 27:
                            tile_sprite = submarine1_sink3
                    elif sink_anim_ticks in range(45, 60):
                        if tile == 25:
                            tile_sprite = submarine3_sink4
                        elif tile == 26:
                            tile_sprite = submarine2_sink4
                        elif tile == 27:
                            tile_sprite = submarine1_sink4
                    elif sink_anim_ticks in range(60, 75):
                        if tile == 25:
                            tile_sprite = submarine3_sink5
                        elif tile == 26:
                            tile_sprite = submarine2_sink5
                        elif tile == 27:
                            tile_sprite = submarine1_sink5

                if cruiser_sink_anim == True:
                    if sink_anim_ticks in range(0, 15):
                        if tile == 35:
                            tile_sprite = cruiser3_sink1
                        elif tile == 36:
                            tile_sprite = cruiser2_sink1
                        elif tile == 37:
                            tile_sprite = cruiser1_sink1
                    elif sink_anim_ticks in range(15, 30):
                        if tile == 35:
                            tile_sprite = cruiser3_sink2
                        elif tile == 36:
                            tile_sprite = cruiser2_sink2
                        elif tile == 37:
                            tile_sprite = cruiser1_sink2
                    elif sink_anim_ticks in range(30, 45):
                        if tile == 35:
                            tile_sprite = cruiser3_sink3
                        elif tile == 36:
                            tile_sprite = cruiser2_sink3
                        elif tile == 37:
                            tile_sprite = cruiser1_sink3
                    elif sink_anim_ticks in range(45, 60):
                        if tile == 35:
                            tile_sprite = cruiser3_sink4
                        elif tile == 36:
                            tile_sprite = cruiser2_sink4
                        elif tile == 37:
                            tile_sprite = cruiser1_sink4
                    elif sink_anim_ticks in range(60, 75):
                        if tile == 35:
                            tile_sprite = cruiser3_sink5
                        elif tile == 36:
                            tile_sprite = cruiser2_sink5
                        elif tile == 37:
                            tile_sprite = cruiser1_sink5
                
                if battleship_sink_anim == True:
                    if sink_anim_ticks in range(0, 15):
                        if tile == 45:
                            tile_sprite = battleship4_sink1
                        elif tile == 46:
                            tile_sprite = battleship3_sink1
                        elif tile == 47:
                            tile_sprite = battleship2_sink1
                        elif tile == 48:
                            tile_sprite = battleship1_sink1
                    elif sink_anim_ticks in range(15, 30):
                        if tile == 45:
                            tile_sprite = battleship4_sink2
                        elif tile == 46:
                            tile_sprite = battleship3_sink2
                        elif tile == 47:
                            tile_sprite = battleship2_sink2
                        elif tile == 48:
                            tile_sprite = battleship1_sink2
                    elif sink_anim_ticks in range(30, 45):
                        if tile == 45:
                            tile_sprite = battleship4_sink3
                        elif tile == 46:
                            tile_sprite = battleship3_sink3
                        elif tile == 47:
                            tile_sprite = battleship2_sink3
                        elif tile == 48:
                            tile_sprite = battleship1_sink3
                    elif sink_anim_ticks in range(45, 60):
                        if tile == 45:
                            tile_sprite = battleship4_sink4
                        elif tile == 46:
                            tile_sprite = battleship3_sink4
                        elif tile == 47:
                            tile_sprite = battleship2_sink4
                        elif tile == 48:
                            tile_sprite = battleship1_sink4
                    elif sink_anim_ticks in range(60, 75):
                        if tile == 45:
                            tile_sprite = battleship4_sink5
                        elif tile == 46:
                            tile_sprite = battleship3_sink5
                        elif tile == 47:
                            tile_sprite = battleship2_sink5
                        elif tile == 48:
                            tile_sprite = battleship1_sink5
                        
                if carrier_sink_anim == True:
                    if sink_anim_ticks in range(0, 15):
                        if tile == 55:
                            tile_sprite = carrier5_sink1
                        elif tile == 56:
                            tile_sprite = carrier4_sink1
                        elif tile == 57:
                            tile_sprite = carrier3_sink1
                        elif tile == 58:
                            tile_sprite = carrier2_sink1
                        elif tile == 59:
                            tile_sprite = carrier1_sink1
                    elif sink_anim_ticks in range(15, 30):
                        if tile == 55:
                            tile_sprite = carrier5_sink2
                        elif tile == 56:
                            tile_sprite = carrier4_sink2
                        elif tile == 57:
                            tile_sprite = carrier3_sink2
                        elif tile == 58:
                            tile_sprite = carrier2_sink2
                        elif tile == 59:
                            tile_sprite = carrier1_sink2
                    elif sink_anim_ticks in range(30, 45):
                        if tile == 55:
                            tile_sprite = carrier5_sink3
                        elif tile == 56:
                            tile_sprite = carrier4_sink3
                        elif tile == 57:
                            tile_sprite = carrier3_sink3
                        elif tile == 58:
                            tile_sprite = carrier2_sink3
                        elif tile == 59:
                            tile_sprite = carrier1_sink3
                    elif sink_anim_ticks in range(45, 60):
                        if tile == 55:
                            tile_sprite = carrier5_sink4
                        elif tile == 56:
                            tile_sprite = carrier4_sink4
                        elif tile == 57:
                            tile_sprite = carrier3_sink4
                        elif tile == 58:
                            tile_sprite = carrier2_sink4
                        elif tile == 59:
                            tile_sprite = carrier1_sink4
                    elif sink_anim_ticks in range(60, 75):
                        if tile == 55:
                            tile_sprite = carrier5_sink5
                        elif tile == 56:
                            tile_sprite = carrier4_sink5
                        elif tile == 57:
                            tile_sprite = carrier3_sink5
                        elif tile == 58:
                            tile_sprite = carrier2_sink5
                        elif tile == 59:
                            tile_sprite = carrier1_sink5

                if tile_sprite == "blank":
                    pass
                elif nuke_anim == True:
                    not_cell = True
                    if (x in [target_cell.x-1, target_cell.x, target_cell.x+1]) and (y in [target_cell.y-1, target_cell.y, target_cell.y+1]):
                        if pygame.Vector2(x, y) != target_cell:
                            if nuke_ticks > 30 and nuke_ticks <= 35:
                                y_level = 10+x*ydil+y*ydil-(nuke_ticks-30)*0.05
                            elif nuke_ticks > 35 and nuke_ticks <= 40:
                                y_level = 10+x*ydil+y*ydil-(40-nuke_ticks)*0.1
                            else:
                                not_cell = False
                        elif pygame.Vector2(x, y) == target_cell:
                            if nuke_ticks > 30 and nuke_ticks <= 40:
                                y_level = 10+x*ydil+y*ydil+(nuke_ticks-30)*0.3
                            else:
                                not_cell = False
                        else:
                            not_cell = False
                    elif (x in [target_cell.x-2, target_cell.x+2] and y in [target_cell.y-2, target_cell.y-1, target_cell.y, target_cell.y+1, target_cell.y+2]) or \
                    (y in [target_cell.y-2, target_cell.y+2] and x in [target_cell.x-1, target_cell.x, target_cell.x+1]):
                        if nuke_ticks > 35 and nuke_ticks <= 40:
                            y_level = 10+x*ydil+y*ydil-(nuke_ticks-35)*0.05
                        elif nuke_ticks > 40 and nuke_ticks <= 45:
                            y_level = 10+x*ydil+y*ydil-(45-nuke_ticks)*0.1
                        else:
                            not_cell = False
                    elif (x in [target_cell.x-3, target_cell.x+3] and y in [target_cell.y-3, target_cell.y-2, target_cell.y-1, target_cell.y, target_cell.y+1, target_cell.y+2, target_cell.y+3]) or \
                    (y in [target_cell.y-3, target_cell.y+3] and x in [target_cell.x-2, target_cell.x-1, target_cell.x, target_cell.x+1, target_cell.x+2]):
                        if nuke_ticks > 40 and nuke_ticks <= 45:
                            y_level = 10+x*ydil+y*ydil-(nuke_ticks-40)*0.05
                        elif nuke_ticks > 45 and nuke_ticks <= 50:
                            y_level = 10+x*ydil+y*ydil-(50-nuke_ticks)*0.1
                        else:
                            not_cell = False
                    else:
                        not_cell = False

                    if not_cell == False:
                        if rotate_cell == False:
                            leftRender.blit(tile_sprite, (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
                        else:
                            leftRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
                    else:
                        if rotate_cell == False:
                            leftRender.blit(tile_sprite, (144+x*xdil-y*xdil, y_level))
                        else:
                            leftRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, y_level))
                    
                elif rotate_cell == False:
                    leftRender.blit(tile_sprite, (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
                else:
                    leftRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))

        # right render
        for y, row in enumerate(P1Boats):
            for x, tile in enumerate(row):
                xdil = 16
                ydil = 8
                boat_type = 9  
                rotate_cell = None              
                if tile in range(10, 20):
                    boat_type = 0
                if tile in range(20, 30):
                    boat_type = 1
                if tile in range(30, 40):
                    boat_type = 2
                if tile in range(40, 50):
                    boat_type = 3
                if tile in range(50, 60):
                    boat_type = 4
                
                if boat_type != 9:
                    if P1Rot[boat_type] == 0:
                        rotate_cell = False
                    elif P1Rot[boat_type] == 1:
                        rotate_cell = True
                
                if tile == 5:
                    if Prev_action != []:
                        in_prev = False
                        for i in Prev_action:
                            if int((i - (i%10))/10) == y and int(i%10) == x:
                                tile_sprite = funcs.get(tile-5, "blank")
                                in_prev = True
                        if in_prev == False:
                            tile_sprite = d_sea_nohit_tile
                    else:
                        tile_sprite = d_sea_nohit_tile
                elif tile in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    in_prev = False
                    if Prev_action != []:
                        for i in Prev_action:
                            if int((i - (i%10))/10) == y and int(i%10) == x:
                                tile_sprite = funcs.get(tile-5, "blank")
                                in_prev = True
                    if in_prev == False:
                        tile_sprite = d_sea_hit_tile
                        hit_tiles = {
                            15: destroyer2_sink5,
                            16: destroyer1_sink5,
                            25: submarine3_sink5,
                            26: submarine2_sink5,
                            27: submarine1_sink5,
                            35: cruiser3_sink5,
                            36: cruiser2_sink5,
                            37: cruiser1_sink5,
                            45: battleship4_sink5,
                            46: battleship3_sink5,
                            47: battleship2_sink5,
                            48: battleship1_sink5,
                            55: carrier5_sink5,
                            56: carrier4_sink5,
                            57: carrier3_sink5,
                            58: carrier2_sink5,
                            59: carrier1_sink5
                        }
                        if (P1Boats_sunk[0] == 1 and tile in [15, 16]) or (P1Boats_sunk[1] == 1 and tile in [25, 26, 27])\
                            or (P1Boats_sunk[2] == 1 and tile in [35, 36, 37]) or (P1Boats_sunk[3] == 1 and tile in [45, 46, 47, 48])\
                            or (P1Boats_sunk[4] == 1 and tile in [55, 56, 57, 58, 59]):
                            tile_sprite = hit_tiles.get(tile, d_sea_hit_tile)
                else:
                    tile_sprite = funcs.get(tile, funcs.get(tile-5, "blank"))

                if tile_sprite == "blank":
                    pass
                elif rotate_cell == False:
                    rightRender.blit(tile_sprite, (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
                else:
                    rightRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))


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
            left_pos = pygame.Vector2(55, 50-(left_size*0.13))
            right_pos = pygame.Vector2(1225-right_size, 670-(right_size*0.69))
            anim_ticks += 1*dbltime
            if nuke_anim2 == True:
                if anim_ticks <= 30:
                    i = target_cell.x
                    j = target_cell.y
                    rightOverlay.blit(pygame.transform.scale_by(nuke_img, (0.4, 0.4)), (144+i*xdil-j*xdil+2, (37+i*ydil+j*ydil) - 5*(30-anim_ticks)))
            elif selectedPlayerMode == False and door_anim == False and P1Boats_sunk == [1, 1, 1, 1, 1] and Prev_action == []:
                    door_anim = True
                    door_ticks = 0
        elif delay < anim_ticks <= delay + t:
            if Prev_action != []:
                x = int(Prev_action[0] % 10)
                y = int((Prev_action[0]-x)/10)
                target_cell = pygame.Vector2(x, y)
                Prev_action.pop(0)
                nuke_anim2 = True
                anim_ticks = 0
            else:
                nuke_anim2 = False
                left_size = screen.get_width()/2 + scale*(1 - (0.5*t - (anim_ticks - delay))*diff)
                right_size = screen.get_width()/2 + scale*(1 + (0.5*t - (anim_ticks - delay))*diff)
                left_pos = pygame.Vector2(55, 50-(left_size*0.13))
                right_pos = pygame.Vector2(1225-right_size, 670-(right_size*0.69))
                anim_ticks += 1*dbltime
        else:
            if nuke_anim == False and destroyer_sink_anim == False and submarine_sink_anim == False\
                and cruiser_sink_anim == False and battleship_sink_anim == False and carrier_sink_anim == False:
                x = selected_cell.x
                y = selected_cell.y
                if P2Boats[int(selected_cell.y)][int(selected_cell.x)] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    leftOverlay.blit(cursorX, (144+x*xdil-y*xdil, -13+x*ydil+y*ydil))
                else:
                    leftOverlay.blit(cursorC, (144+x*xdil-y*xdil, -13+x*ydil+y*ydil))
                nuke_ticks = 0
                if door_anim == False and P2Boats_sunk == [1, 1, 1, 1, 1]:
                    door_anim = True
                    door_ticks = 0

            if keys[pygame.K_SPACE] and nuke_anim == False and destroyer_sink_anim == False and submarine_sink_anim == False\
                and cruiser_sink_anim == False and battleship_sink_anim == False and carrier_sink_anim == False:
                if P2Boats[int(selected_cell.y)][int(selected_cell.x)] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    pass
                else:
                    nuke_anim = True
                    sink_anim_ticks = 0

            if nuke_anim == True:
                x = int(selected_cell.x)
                y = int(selected_cell.y)
                target_cell = pygame.Vector2(x, y)
                if nuke_ticks <= 30:
                    leftOverlay.blit(pygame.transform.scale_by(nuke_img, (0.4, 0.4)), (144+x*xdil-y*xdil+2, (-13+x*ydil+y*ydil) - 5*(30-nuke_ticks)))
                if P2Boats[y][x] in [10, 11, 20, 21, 22, 30, 31, 32, 40, 41, 42, 43, 50, 51, 52, 53, 54]:
                    if nuke_ticks == 31:
                        sound_list = [
                            explosion_sfx1, explosion_sfx2, explosion_sfx3, explosion_sfx4
                        ]
                        pygame.mixer.Sound.play(sound_list[random.randint(0, 3)])
                    if nuke_ticks in range(31, 78):
                        if nuke_ticks in range(31, 33):
                            explosion_img = explosion_frame_1
                        elif nuke_ticks in range(33, 35):
                            explosion_img = explosion_frame_2
                        elif nuke_ticks in range(35, 37):
                            explosion_img = explosion_frame_3
                        elif nuke_ticks in range(37, 41):
                            explosion_img = explosion_frame_4
                        elif nuke_ticks in range(41, 45):
                            explosion_img = explosion_frame_5
                        elif nuke_ticks in range(45, 49):
                            explosion_img = explosion_frame_6
                        elif nuke_ticks in range(53, 57):
                            explosion_img = explosion_frame_7
                        elif nuke_ticks in range(57, 61):
                            explosion_img = explosion_frame_8
                        elif nuke_ticks in range(61, 65):
                            explosion_img = explosion_frame_9
                        elif nuke_ticks in range(65, 69):
                            explosion_img = explosion_frame_10
                        elif nuke_ticks in range(69, 73):
                            explosion_img = explosion_frame_11
                        elif nuke_ticks in range(73, 77):
                            explosion_img = explosion_frame_12
                        leftOverlay.blit(pygame.transform.scale_by(explosion_img, (1, 1)), (126+x*xdil-y*xdil+2, -10+x*ydil+y*ydil))
                else:
                    if nuke_ticks == 31:
                        sound_list = [
                            splash_sfx1, splash_sfx2, splash_sfx3, splash_sfx4, splash_sfx5
                        ]
                        pygame.mixer.Sound.play(sound_list[random.randint(0, 4)])
                    if nuke_ticks in range(31, 68):
                        if nuke_ticks in range(31, 34):
                            splash_img = splash_frame_1
                        elif nuke_ticks in range(34, 37):
                            splash_img = splash_frame_2
                        elif nuke_ticks in range(37, 40):
                            splash_img = splash_frame_3
                        elif nuke_ticks in range(40, 43):
                            splash_img = splash_frame_4
                        elif nuke_ticks in range(43, 46):
                            splash_img = splash_frame_5
                        elif nuke_ticks in range(46, 49):
                            splash_img = splash_frame_6
                        elif nuke_ticks in range(49, 52):
                            splash_img = splash_frame_7
                        elif nuke_ticks in range(52, 55):
                            splash_img = splash_frame_8
                        if nuke_ticks in range(55, 58):
                            splash_img = splash_frame_9
                        elif nuke_ticks in range(58, 61):
                            splash_img = splash_frame_10
                        elif nuke_ticks in range(61, 64):
                            splash_img = splash_frame_11
                        elif nuke_ticks in range(64, 67):
                            splash_img = splash_frame_12
                        leftOverlay.blit(pygame.transform.scale_by(splash_img, (0.75, 0.75)), (134+x*xdil-y*xdil+2, -12+x*ydil+y*ydil))

                nuke_ticks += 1*dbltime

                if nuke_ticks > 120:
                    P2Boats[y][x] += 5
                    nuke_anim = False
                    if any(15 in sl for sl in P2Boats) and any(16 in sl for sl in P2Boats) and P2Boats_sunk[0] == 0:
                        destroyer_sink_anim = True
                        P2Boats_sunk[0] = 1
                    elif any(25 in sl for sl in P2Boats) and any(26 in sl for sl in P2Boats) and any(27 in sl for sl in P2Boats) and P2Boats_sunk[1] == 0:
                        submarine_sink_anim = True
                        P2Boats_sunk[1] = 1
                    elif any(35 in sl for sl in P2Boats) and any(36 in sl for sl in P2Boats) and any(37 in sl for sl in P2Boats) and P2Boats_sunk[2] == 0:
                        cruiser_sink_anim = True
                        P2Boats_sunk[2] = 1
                    elif any(45 in sl for sl in P2Boats) and any(46 in sl for sl in P2Boats) and any(47 in sl for sl in P2Boats) and any(48 in sl for sl in P2Boats) and P2Boats_sunk[3] == 0:
                        battleship_sink_anim = True
                        P2Boats_sunk[3] = 1
                    elif any(55 in sl for sl in P2Boats) and any(56 in sl for sl in P2Boats) and any(57 in sl for sl in P2Boats) and any(58 in sl for sl in P2Boats) and any(59 in sl for sl in P2Boats) and P2Boats_sunk[4] == 0:
                        carrier_sink_anim = True
                        P2Boats_sunk[4] = 1
                    if P2Boats[y][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                        pass
                    else:
                        Prev_action = []
                        switch("page router")

            if destroyer_sink_anim == True:
                sink_anim_ticks += 1*dbltime
                
                if sink_anim_ticks == 1:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                if sink_anim_ticks > 120:
                    destroyer_sink_anim = False
            
            if submarine_sink_anim == True:
                sink_anim_ticks += 1*dbltime
                
                if sink_anim_ticks == 1:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                if sink_anim_ticks > 120:
                    submarine_sink_anim = False

            if cruiser_sink_anim == True:
                sink_anim_ticks += 1*dbltime
                
                if sink_anim_ticks == 1:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                if sink_anim_ticks > 120:
                    cruiser_sink_anim = False
            
            if battleship_sink_anim == True:
                sink_anim_ticks += 1*dbltime
                
                if sink_anim_ticks == 1:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                if sink_anim_ticks > 120:
                    battleship_sink_anim = False
            
            if carrier_sink_anim == True:
                sink_anim_ticks += 1*dbltime
                
                if sink_anim_ticks == 1:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                if sink_anim_ticks > 120:
                    carrier_sink_anim = False
                    
        if selectedPlayerMode == False:
            if difficulty == "Easy":
                hud.blit(hud_P1A1_img, (0, 0))
            else:
                hud.blit(hud_P1A2_img, (0, 0))
        else:
            hud.blit(hud_P1P2_img, (0, 0))

        if door_anim == True:
            
            f = 2
            if door_ticks // f <= f*0:
                switch_door = widgets.Image(640, 360, blast_door_8, 1)
            elif door_ticks // f == f*1:
                switch_door = widgets.Image(640, 360, blast_door_7, 1)
            elif door_ticks // f == f*2:
                switch_door = widgets.Image(640, 360, blast_door_6, 1)
            elif door_ticks // f == f*3:
                switch_door = widgets.Image(640, 360, blast_door_5, 1)
            elif door_ticks // f == f*4:
                switch_door = widgets.Image(640, 360, blast_door_4, 1)
            elif door_ticks// f == f*5:
                switch_door = widgets.Image(640, 360, blast_door_3, 1)
            elif door_ticks // f == f*6:
                switch_door = widgets.Image(640, 360, blast_door_2, 1)
            elif door_ticks // f == f*7:
                switch_door = widgets.Image(640, 360, blast_door_1, 1)
            
            switch_door.draw(hud)

            if door_ticks > 30:
                door_anim = False
                switch("page router")

            door_ticks += 1
    
    elif game_screen == "win":
        draw_text(f"Winner: {winner}", font1, (0, 0, 0), (1280-font1.size(f"Winner: {winner}")[0])/2, 100)
        if door_anim == True:
            f = 2
            if door_ticks // f <= f*0:
                switch_door = widgets.Image(640, 360, blast_door_1, 1)
            elif door_ticks // f == f*1:
                switch_door = widgets.Image(640, 360, blast_door_2, 1)
            elif door_ticks // f == f*2:
                switch_door = widgets.Image(640, 360, blast_door_3, 1)
            elif door_ticks // f == f*3:
                switch_door = widgets.Image(640, 360, blast_door_4, 1)
            elif door_ticks // f == f*4:
                switch_door = widgets.Image(640, 360, blast_door_5, 1)
            elif door_ticks// f == f*5:
                switch_door = widgets.Image(640, 360, blast_door_6, 1)
            elif door_ticks // f == f*6:
                switch_door = widgets.Image(640, 360, blast_door_7, 1)
            elif door_ticks // f == f*7:
                switch_door = widgets.Image(640, 360, blast_door_8, 1)
            
            switch_door.draw(hud)

            if door_ticks > 30:
                door_anim = False

            door_ticks += 1
        

    # animate water
    if sea_anim_cd <= 0:
        cur_sea += 1
        if cur_sea == 3:
            cur_sea = 0
        tiles: list = [sea_tile1,
                       sea_tile2,
                       sea_tile3,
                       sea_nohit_tile1,
                       sea_nohit_tile2,
                       sea_nohit_tile3,
                       sea_hit_tile1,
                       sea_hit_tile2,
                       sea_hit_tile3
        ]
        d_sea_tile = tiles[cur_sea]
        d_sea_nohit_tile = tiles[cur_sea+3]
        d_sea_hit_tile = tiles[cur_sea+6]
        sea_anim_cd = 15
    
    sea_anim_cd -= 1
    
    dt = clock.tick(60) / 1000
    screen.blit(pygame.transform.scale(placementSurface, (screen.get_width()/1.4, screen.get_width()/1.4)), (380, 50))
    screen.blit(pygame.transform.scale(leftRender, (left_size, left_size)), left_pos)
    screen.blit(pygame.transform.scale(leftOverlay, (left_size, left_size)), (55, 0))
    screen.blit(pygame.transform.scale(rightRender, (right_size, right_size)), right_pos)
    screen.blit(pygame.transform.scale(rightOverlay, (right_size, right_size)), (right_pos.x, 0))
    screen.blit(hud, (0, 0))
    try:
        org_screen.blit(screen, next(offset))
    except:
        org_screen.blit(screen, (0, 0))
    
    pygame.display.update()

pygame.quit()