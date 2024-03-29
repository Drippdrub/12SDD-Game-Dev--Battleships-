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

Tk().wm_withdraw() #hide Tkinter main window, only messagebox is needed

# set screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# used for pyinstaller compatability
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# initialise pygame
pygame.init()
# randomised window caption
captions = [": Sinking Hopes and Dreams", ": Battleships? What's that?", ": Water Warfare",
            " 2: Electric Boogaloo", " 3: Revenge of the Sith", ""]
pygame.display.set_caption(f"Steel and Salvos{random.choice(captions)}")
programIcon = pygame.image.load(resource_path('images/Icon.png'))
pygame.display.set_icon(programIcon)

# set surfaces
org_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32) #parent screen
screen = org_screen.copy() #buffer screen, used to screen-shake. All children are blit to this surface, and this surface is blit to org_screen
hud = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA, 32).convert_alpha() #overlay surface. blit last, so all object in this layer are always on top
leftRender = pygame.Surface((320, 320)).convert_alpha() #renders leftside grid in game
leftOverlay = pygame.Surface((320, 320)).convert_alpha() #renders cursor, bombs and animations on top of leftside grid in game
rightRender = pygame.Surface((320, 320)).convert_alpha() #renders rightside grid in game
rightOverlay = pygame.Surface((320, 320)).convert_alpha() #renders bombs and animations on top of rightside grid in game
placementSurface = pygame.Surface((400, 400)).convert_alpha() #renders grid for boat placement

clock = pygame.time.Clock() #clock object

# event to detect when music has stopped playing
SONG_FINISHED = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_FINISHED)

# draw text to screen
def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    hud.blit(img, (x, y))

# offset used for screen shake, is (0, 0) by default (aka no displacement)
offset = repeat((0, 0))
# shake function
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

# font imports
font1 = pygame.font.Font(resource_path("fonts\CompassPro.ttf"), 72)
font2 = pygame.font.Font(resource_path("fonts\Crang.ttf"), 84)
font3 = pygame.font.Font(resource_path("fonts\CompassPro.ttf"), 36)
font4 = pygame.font.Font(resource_path("fonts\CompassPro.ttf"), 28)
font5 = pygame.font.Font(resource_path("fonts\CompassPro.ttf"), 18)

# set default sound levels
master_lvl = 1.0
sfx_lvl = 0.75
music_lvl = 0.75

# sfx imports
# metal door sounds
door_open_sfx = pygame.mixer.Sound(resource_path("sounds\SFX\door open.mp3"))
door_open_sfx.set_volume(0.75)
door_close_sfx = pygame.mixer.Sound(resource_path("sounds\SFX\door close.mp3"))
door_close_sfx.set_volume(0.75)

# startup sounds
startup_sfx1 = pygame.mixer.Sound(resource_path("sounds/SFX/Explosion1.wav"))
startup_sfx1.set_volume(0.75)
startup_sfx2 = pygame.mixer.Sound(resource_path("sounds\SFX\Blip1.wav"))
startup_sfx2.set_volume(0.75)
music_unending = pygame.mixer.music.load(resource_path("sounds/Music/unending.wav"))

# button press sound 
blip = pygame.mixer.Sound(resource_path("sounds\SFX\Blip2.wav"))
blip.set_volume(0.75)

# boat placement sounds
place_sfx1 = pygame.mixer.Sound(resource_path("sounds\SFX\place.wav"))
place_sfx1.set_volume(0.75)
denyClick_sfx1 = pygame.mixer.Sound(resource_path("sounds\SFX\DenyClick.wav"))
denyClick_sfx1.set_volume(0.75)

# boat sinking sound
sink_sfx1 = pygame.mixer.Sound(resource_path("sounds\SFX\Sink.wav"))
sink_sfx1.set_volume(0.75)

# boat hit (explosion) sounds
explosion_sfx1 = pygame.mixer.Sound(resource_path("sounds\SFX\Explosion1.wav"))
explosion_sfx1.set_volume(0.75)
explosion_sfx2 = pygame.mixer.Sound(resource_path("sounds\SFX\Explosion2.wav"))
explosion_sfx2.set_volume(0.75)
explosion_sfx3 = pygame.mixer.Sound(resource_path("sounds\SFX\Explosion3.wav"))
explosion_sfx3.set_volume(0.75)
explosion_sfx4 = pygame.mixer.Sound(resource_path("sounds\SFX\Explosion4.wav"))
explosion_sfx4.set_volume(0.75)

# boat miss (splash) sounds
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

# image imports
# button assets
playButton_img = pygame.image.load(resource_path("images/button_play.png")).convert_alpha()
playButton_hover = pygame.image.load(resource_path("images/button_play_hover.png")).convert_alpha()
optionButton_img = pygame.image.load(resource_path("images/button_options.png")).convert_alpha()
optionButton_hover = pygame.image.load(resource_path("images/button_options_hover.png")).convert_alpha()
creditsButton_img = pygame.image.load(resource_path("images/button_credits.png")).convert_alpha()
creditsButton_hover = pygame.image.load(resource_path("images/button_credits_hover.png")).convert_alpha()
exitButton_img = pygame.image.load(resource_path("images/button_exit.png")).convert_alpha()
exitButton_hover = pygame.image.load(resource_path("images/button_exit_hover.png")).convert_alpha()
backButton_img = pygame.image.load(resource_path("images/button_back.png")).convert_alpha()
backButton_hover = pygame.image.load(resource_path("images/button_back_hover.png")).convert_alpha()
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
resumeButton_img = pygame.image.load(resource_path("images/button_resume.png")).convert_alpha()
resumeButton_hover = pygame.image.load(resource_path("images/button_resume_hover.png")).convert_alpha()
option2Button_img = pygame.image.load(resource_path("images/button_options2.png")).convert_alpha()
option2Button_hover = pygame.image.load(resource_path("images/button_options_hover2.png")).convert_alpha()
leaveButton_img = pygame.image.load(resource_path("images/button_leave.png")).convert_alpha()
leaveButton_hover = pygame.image.load(resource_path("images/button_leave_hover.png")).convert_alpha()

timeoff_img = pygame.image.load(resource_path("images/time_off.png")).convert_alpha()
time60s_img = pygame.image.load(resource_path("images/time_60.png")).convert_alpha()
time90s_img = pygame.image.load(resource_path("images/time_90.png")).convert_alpha()
time3m_img = pygame.image.load(resource_path("images/time_3m.png")).convert_alpha()
time5m_img = pygame.image.load(resource_path("images/time_5m.png")).convert_alpha()
time10m_img = pygame.image.load(resource_path("images/time_10m.png")).convert_alpha()

help_icon = pygame.image.load(resource_path("images/help.png")).convert_alpha()

fps30_img = pygame.image.load(resource_path("images/fps30.png")).convert_alpha()
fps60_img = pygame.image.load(resource_path("images/fps60.png")).convert_alpha()
fps120_img = pygame.image.load(resource_path("images/fps120.png")).convert_alpha()

# player card assets
player1Board_img = pygame.image.load(resource_path("images\Player1 Board.png")).convert_alpha()
player2Board_img = pygame.image.load(resource_path("images\Player2 Board.png")).convert_alpha()
ai_easy_Board_img = pygame.image.load(resource_path("images\AI Easy Board.png")).convert_alpha()
ai_hard_Board_img = pygame.image.load(resource_path("images\AI Hard Board.png")).convert_alpha()

# empty boxes
middle_Board_img = pygame.image.load(resource_path("images\Middle Board.png")).convert_alpha()
big_Board_img = pygame.image.load(resource_path("images\Big Board.png")).convert_alpha()
left_Board_img = pygame.image.load(resource_path("images\Left Board.png")).convert_alpha()
split_Board_img = pygame.image.load(resource_path("images\Split Board.png")).convert_alpha()

# player icons
player1_img = pygame.image.load(resource_path("images\Icons\Player1.png")).convert_alpha()
player2_img = pygame.image.load(resource_path("images\Icons\Player2.png")).convert_alpha()
aiEasy_img = pygame.image.load(resource_path("images\Icons\AIE.png")).convert_alpha()
aiHard_img = pygame.image.load(resource_path("images\Icons\AIH.png")).convert_alpha()

# button icons
controls_wasd_img = pygame.image.load(resource_path("images\Instructions/WASD.png")).convert_alpha()
controls_numbers_img = pygame.image.load(resource_path("images\Instructions/Numbers.png")).convert_alpha()
controls_shift_img = pygame.image.load(resource_path("images\Instructions/Shift.png")).convert_alpha()
controls_r_img = pygame.image.load(resource_path("images\Instructions/R.png")).convert_alpha()
controls_e_img = pygame.image.load(resource_path("images\Instructions/E.png")).convert_alpha()
controls_f_img = pygame.image.load(resource_path("images\Instructions/F.png")).convert_alpha()
controls_space_img = pygame.image.load(resource_path("images\Instructions/Space.png")).convert_alpha()

# in game hud assets
hud_P1P2_img = pygame.image.load(resource_path("images\Huds\Hud1.png")).convert_alpha()
hud_P2P1_img = pygame.image.load(resource_path("images\Huds\Hud4.png")).convert_alpha()
hud_P1A1_img = pygame.image.load(resource_path("images\Huds\Hud2.png")).convert_alpha()
hud_P1A2_img = pygame.image.load(resource_path("images\Huds\Hud3.png")).convert_alpha()
hud_time_img = pygame.image.load(resource_path("images\Huds\HudTime.png")).convert_alpha()

# background images
ocean_screen = pygame.image.load(resource_path("images/Ocean.png")).convert_alpha()
metal_screen = pygame.image.load(resource_path("images\metal bg.png")).convert_alpha()

# photosensitive seizure warning screen
psw_img = pygame.image.load(resource_path("images\PSW.png")).convert_alpha()

# credits screen
credits_img = pygame.image.load(resource_path("images/Credits.png"))

# mute/unmute button
mute_img = pygame.image.load(resource_path("images/mute.png")).convert_alpha()
unmute_img = pygame.image.load(resource_path("images/unmute.png")).convert_alpha()

# turn banner assets
turn_banner_You = pygame.image.load(resource_path("images/turn banner1.png")).convert_alpha()
turn_banner_Opp = pygame.image.load(resource_path("images/turn banner2.png")).convert_alpha()

# pause icon
pause_icon = pygame.image.load(resource_path("images/Pause.png")).convert_alpha()

# bomb asset
nuke_img = pygame.image.load(resource_path("images/nuke.png")).convert_alpha()

# metal door asset + screen fade
black_screen = pygame.image.load(resource_path("images/black_screen.png")).convert_alpha()
blast_door_1 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door1.png")).convert_alpha()
blast_door_2 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door2.png")).convert_alpha()
blast_door_3 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door3.png")).convert_alpha()
blast_door_4 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door4.png")).convert_alpha()
blast_door_5 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door5.png")).convert_alpha()
blast_door_6 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door6.png")).convert_alpha()
blast_door_7 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door7.png")).convert_alpha()
blast_door_8 = pygame.image.load(resource_path("images\Anims\Blast Door/blast_door8.png")).convert_alpha()

# explosion animation frames
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

# splash animation frames
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

# test iso sprites
# iso_test = pygame.image.load(resource_path("images\iso_test.png")).convert_alpha()
# ship_tile = pygame.image.load(resource_path("images\isometric tiles\ship unit.png")).convert_alpha()

# boat placement boat labels
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
player1_gridlabel = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Player1.png")).convert_alpha()
player2_gridlabel = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Player2.png")).convert_alpha()
computer_gridlabel = pygame.image.load(resource_path("images\isometric tiles\Grid Labels\Computer.png")).convert_alpha()

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

# import boat/grid assets + sinking animations
cursorC = pygame.image.load(resource_path("images\isometric tiles\cursorC.png")).convert_alpha()
cursorX = pygame.image.load(resource_path("images\isometric tiles\cursorX.png")).convert_alpha()

# destroyer (2 long)
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

# submarine (3 long)
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

# cruiser (3 long)
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

# battleship (4 long)
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

# carrier (5 long)
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


# set starting game screen to photosensitive seizure warning screen
game_screen = "PSW"

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
# empty boat grids, will be filled later
PlacingGrid = []
P1Boats = []
P2Boats = []

# function to switch game screen, also prints for debug
def switch(screen):
    global game_screen
    game_screen = screen
    print(screen)

psw_ticks = 0
rounded_startup_ticks = 0
startup_ticks = 0
startup_played = [0, 0, 0, 0, 0, 0]

selectedPlayerMode = True
difficulty = "Easy"
time_enabled = False
time_set = 0
dbltime = 1 #used for dev bugtesting, anims play at double time when set to 2.
# this however breaks sounds. setting to any other value other than 1 or 2 may break the game completely
devmode = 1 #used for dev bugtesting, mostly used for viewing ship grids, 1 to enable, 0 to disable
dev_sustain = 0
unfairness_multiplier = 0 #number form 0-10, increases chance that the AI will automatically target a ship, used to speed up games

inGame = False
playersReady = 0

prompt_cd = 0

StoredBoats = [1, 1, 1, 1, 1] #checks which boats are on field during placement
BoatRotation = [0, 0, 0, 0, 0] # stores boat directions during placement, 0 to the right, 1 to the left
selected_boat = 0
cur_boat_len = 2
selected_cell = pygame.Vector2(0,0)
mov_cd = 0
rot_cd = 0
cursor_dir = 0
swap_cd = 0
bad_cell = False
stamp_cd = 0
deselect_cd = 0

P1Rot = []
P2Rot = []

turn = 0
rounded_anim_ticks = 0
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
down = 20
backButton = widgets.Button(110, 75, backButton_img, 2, backButton_hover)
masterVolume = slider.Slider(500, 250, 500, master_lvl)
masterMute = widgets.Toggle(400, 250+down, unmute_img, mute_img, 1.25)
musicVolume = slider.Slider(500, 375, 500, music_lvl)
musicMute = widgets.Toggle(400, 375+down, unmute_img, mute_img, 1.25)
sfxVolume = slider.Slider(500, 500, 500, sfx_lvl)
sfxMute = widgets.Toggle(400, 500+down, unmute_img, mute_img, 1.25)
space = 85
fps30 = widgets.Button(1280/1.5-space, 160, fps30_img, 1.5)
fps60 = widgets.Button(1280/1.5, 160, fps60_img, 1.5)
fps120 = widgets.Button(1280/1.5+space, 160, fps120_img, 1.5)

# game options widgets
space = 75
timeOff = widgets.Button(640-space, 260, timeoff_img, 1.3)
time60s = widgets.Button(640, 260, time60s_img, 1.3)
time90s = widgets.Button(640+space, 260, time90s_img, 1.3)
time3m = widgets.Button(640-space, 300, time3m_img, 1.3)
time5m= widgets.Button(640, 300, time5m_img, 1.3)
time10m = widgets.Button(640+space, 300, time10m_img, 1.3)
helpTime = widgets.Image(640+space+50, 260, help_icon, 0.75, "Overall time each player gets in a game.")

selectPlayer = widgets.Toggle(640, 375, select1P_img, select2P_img, 1.2)
selectDiff = widgets.Toggle(640, 475, selectDiffEasy_img, selectDiffHard_img, 0.7)
gameOptionsProceed = widgets.Button(640, 565, playButton_img, 2.75, playButton_hover)
backButton2 = widgets.Button(640, 630, backButton_img, 1.3, backButton_hover)

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
destroyer_indicator_P = widgets.Image(250, 60, lbl_destroyer_placed, 0.9)
destroyer_indicator_S = widgets.Image(250, 60, lbl_destroyer_stored, 0.9)
sub_indicator_S = widgets.Image(250, 100, lbl_sub_stored, 0.9)
sub_indicator_P = widgets.Image(250, 100, lbl_sub_placed, 0.9)
cruiser_indicator_S = widgets.Image(250, 140, lbl_cruiser_stored, 0.9)
cruiser_indicator_P = widgets.Image(250, 140, lbl_cruiser_placed, 0.9)
battleship_indicator_S = widgets.Image(250, 180, lbl_battleship_stored, 0.9)
battleship_indicator_P = widgets.Image(250, 180, lbl_battleship_placed, 0.9)
carrier_indicator_S = widgets.Image(250, 220, lbl_carrier_stored, 0.9)
carrier_indicator_P = widgets.Image(250, 220, lbl_carrier_placed, 0.9)

confirmFleet_button = widgets.Button(1050, 650, confirmFleet_img, 3, confirmFleet_hover)
randomiseFleet_button = widgets.Button(600, 650, randomiseFleet_img, 3, randomiseFleet_hover)

# pause widgets
resume_button = widgets.Button(640, 200, resumeButton_img, 2, resumeButton_hover)
option2_button = widgets.Button(640, 300, option2Button_img, 2, option2Button_hover)
leave_button = widgets.Button(640, 400, leaveButton_img, 2, leaveButton_hover)

# game widgets
pause_button = widgets.Button(50, 50, pause_icon, 2)

# win screen widgets
P1Icon = widgets.Image(320, 325, player1_img, 1.75)
P2Icon = widgets.Image(320, 325, player2_img, 1.75)
AI1Icon = widgets.Image(320, 325, aiEasy_img, 1.75)
AI2Icon = widgets.Image(320, 325, aiHard_img, 1.75)
backButton3 = widgets.Button(960, 625, backButton_img, 1.5, backButton_hover)

gameSongs = ["sounds/Music/Blackmoor Tides.mp3", "sounds/Music/Enemy Ship Approaching.ogg"]
menuSongs = ["sounds/Music/restless sea.wav", "sounds/Music/unending.wav"]

scroll = 0
running = True
FPS = 30
dt = clock.tick(FPS) / 1000
print(f"delta time: {dt}")
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
        elif event.type == SONG_FINISHED and pygame.mixer.music.get_busy() == False:
            if inGame == True:
                pygame.mixer.music.load(resource_path(random.choice(gameSongs)))
            else:
                pygame.mixer.music.load(resource_path(random.choice(menuSongs)))
            pygame.mixer.music.play()

    if game_screen == "PSW":
        if True in pygame.key.get_pressed():
            switch("main")

        screen.blit(pygame.transform.scale(psw_img, (1280, 720)), (0, 0))
        if round(psw_ticks) in range (200, 400):
            black.draw(screen, 1.25*(round(psw_ticks)-200))

        psw_ticks += 1 * 60 * dt

        if psw_ticks >= 400:
            switch("main")

    elif game_screen == "main":
        playersReady = 0

        scale = 1
        bg_tile = math.ceil(SCREEN_WIDTH/(1280*scale))+1
        if rounded_startup_ticks in range(0, 257):
            screen.blit(pygame.transform.scale(ocean_screen, (1280*scale, 720*scale)), (0, 0))
        else:
            for i in range(0, bg_tile):
                screen.blit(pygame.transform.scale(ocean_screen, (1280*scale, 720*scale)), (i * 1280*scale + scroll, 0))
        
        scroll -= 1 * 60 * dt

        if abs(scroll) > 1280:
            scroll = 0

        delay = 130
        if rounded_startup_ticks in range(0, delay+30):
            f = 2
            if (rounded_startup_ticks-delay) // f <= f*0:
                startup_door = widgets.Image(640, 360, blast_door_1, 1)
            elif (rounded_startup_ticks-delay) // f == f*1:
                startup_door = widgets.Image(640, 360, blast_door_2, 1)
            elif (rounded_startup_ticks-delay) // f == f*2:
                startup_door = widgets.Image(640, 360, blast_door_3, 1)
            elif (rounded_startup_ticks-delay) // f == f*3:
                startup_door = widgets.Image(640, 360, blast_door_4, 1)
            elif (rounded_startup_ticks-delay) // f == f*4:
                startup_door = widgets.Image(640, 360, blast_door_5, 1)
            elif (rounded_startup_ticks-delay) // f == f*5:
                startup_door = widgets.Image(640, 360, blast_door_6, 1)
            elif (rounded_startup_ticks-delay) // f == f*6:
                startup_door = widgets.Image(640, 360, blast_door_7, 1)
            elif (rounded_startup_ticks-delay) // f == f*7:
                startup_door = widgets.Image(640, 360, blast_door_8, 1)
            
            startup_door.draw(screen)
        
        if rounded_startup_ticks <= 100:
            black.draw(screen, 250-2.5*rounded_startup_ticks)

        if rounded_startup_ticks >= 1 and pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
        
        if rounded_startup_ticks == 20 and startup_played[5] == 0:
            pygame.mixer.Sound.play(door_open_sfx)
            startup_played[5] = 1

        delay = 217
        duration = 40
        if delay < rounded_startup_ticks < delay+duration:
            font2 = pygame.font.Font(resource_path("fonts\Crang.ttf"), (84+((delay+duration-rounded_startup_ticks)*6)))
        else:
            font2 = pygame.font.Font(resource_path("fonts\Crang.ttf"), 84)
        if rounded_startup_ticks >= delay+duration:
            if startup_played[0] == 0:
                 pygame.mixer.Sound.play(startup_sfx1)
                 startup_played[0] = 1
        
        if rounded_startup_ticks > delay:
            draw_text("Steel and Salvos", font2, (0, 0, 0), (1280-font2.size("Steel and Salvos")[0])/2, 50)

        pause = 14
        interval = 10
        if rounded_startup_ticks >= delay+pause+duration+interval:
             if startup_played[1] == 0:
                 pygame.mixer.Sound.play(startup_sfx2)
                 startup_played[1] = 1
             if playGame.draw(screen):
                 pygame.mixer.Sound.play(blip)
                 switch("game options")
        
        if rounded_startup_ticks >= delay+pause+duration+interval*2:
            if startup_played[2] == 0:
                 pygame.mixer.Sound.play(startup_sfx2)
                 startup_played[2] = 1
            if optionsButton.draw(screen):
                pygame.mixer.Sound.play(blip)
                switch("options")

        if rounded_startup_ticks >= delay+pause+duration+interval*3:
            if startup_played[3] == 0:
                 pygame.mixer.Sound.play(startup_sfx2)
                 startup_played[3] = 1
            if openCredits.draw(screen):
                pygame.mixer.Sound.play(blip)
                switch("credits")

        if rounded_startup_ticks >= delay+pause+duration+interval*4:
            if startup_played[4] == 0:
                 pygame.mixer.Sound.play(startup_sfx2)
                 startup_played[4] = 1
            if exitGame.draw(screen):
                pygame.mixer.Sound.play(blip)
                if messagebox.askokcancel("Close Game?", "You are about to leave the game. Continue?"):
                    running = False

        startup_ticks += 1 * 60 * dt
        rounded_startup_ticks = round(startup_ticks)

    elif game_screen == "options":
        screen.blit(pygame.transform.scale(ocean_screen, (1280*scale, 720*scale)), (0, 0))
        screen.blit(big_Board_img, (0, 0))

        draw_text("Sound Options", font1, (0, 0, 0), (1280-font1.size("Sound Options")[0])/3, 50)
        draw_text("FPS", font1, (0, 0, 0), 1280/1.5-font1.size("FPS")[0]/2, 50)

        if backButton.draw(hud):
            pygame.mixer.Sound.play(blip)
            switch("main")
        
        draw_text("Master Volume", font3, (0, 0, 0), 100, 250)
        master_lvl = round(masterVolume.draw(hud), 2)
        draw_text(f"{master_lvl}", font3, (0, 0, 0), 1050, 250)
        if masterMute.draw(hud) == True:
            master_lvl = 0


        draw_text("Music Volume", font3, (0, 0, 0), 100, 375)
        music_lvl = round(musicVolume.draw(hud), 2)
        draw_text(f"{music_lvl}", font3, (0, 0, 0), 1050, 375)
        if musicMute.draw(hud) == True:
            music_lvl = 0

        pygame.mixer.music.set_volume(music_lvl*master_lvl)


        draw_text("SFX Volume", font3, (0, 0, 0), 100, 500)
        sfx_lvl = round(sfxVolume.draw(hud), 2)
        draw_text(f"{sfx_lvl}", font3, (0, 0, 0), 1050, 500)
        if sfxMute.draw(hud) == True:
            sfx_lvl = 0

        door_open_sfx.set_volume(0.75)
        door_close_sfx.set_volume(0.75)
        startup_sfx1.set_volume(sfx_lvl*master_lvl)
        startup_sfx2.set_volume(sfx_lvl*master_lvl)
        blip.set_volume(sfx_lvl*master_lvl)
        widgets.changeBlip(sfx_lvl*master_lvl)
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

        fps_rates = [30, 60, 120]
        fpsBtns = [fps30, fps60, fps120]
        for fps in fps_rates:
            if FPS == fps:
                fpsBtns[fps_rates.index(fps)].draw(hud, 255)
            else:
                if fpsBtns[fps_rates.index(fps)].draw(hud, 100):
                    FPS = fps
                    pygame.mixer.Sound.play(blip)

    elif game_screen == "credits":
        screen.blit(pygame.transform.scale(ocean_screen, (1280*scale, 720*scale)), (0, 0))
        screen.blit(big_Board_img, (0, 0))
        screen.blit(credits_img, (0, 0))

        if backButton.draw(hud):
            pygame.mixer.Sound.play(blip)
            switch("main")

    elif game_screen == "game options":
        middleBoard.draw(hud)

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

        draw_text("Game Options", font1, (0, 0, 0), (1280-font1.size("Game Options")[0])/2, 100)
        draw_text("Timed Game", font3, (0, 0, 0), (1280-font3.size("Timed Game")[0])/2, 200)
        if time_enabled == False:
            timeOff.draw(hud, 255)
            if time60s.draw(hud, 100):
                time_enabled = True
                time_set = 60
                pygame.mixer.Sound.play(blip)
            if time90s.draw(hud, 100):
                time_enabled = True
                time_set = 90
                pygame.mixer.Sound.play(blip)
            if time3m.draw(hud, 100):
                time_enabled = True
                time_set = 180
                pygame.mixer.Sound.play(blip)
            if time5m.draw(hud, 100):
                time_enabled = True
                time_set = 300
                pygame.mixer.Sound.play(blip)
            if time10m.draw(hud, 100):
                time_enabled = True
                time_set = 600
                pygame.mixer.Sound.play(blip)
        else:
            if timeOff.draw(hud, 100):
                time_enabled = False
                time_set = 0
                pygame.mixer.Sound.play(blip)
            times = [60, 90, 180, 300, 600]
            timeBtns = [time60s, time90s, time3m, time5m, time10m]
            for time in times:
                if time_set == time:
                    timeBtns[times.index(time)].draw(hud, 255)
                else:
                    if timeBtns[times.index(time)].draw(hud, 100):
                        time_set = time
                        pygame.mixer.Sound.play(blip)
        
        helpTime.focusCheck(pygame.mouse.get_pos(), False)
        helpTime.draw(hud)
        helpTime.showTip(hud)
        selectedPlayerMode = selectPlayer.draw(hud, output=0)
        
        if gameOptionsProceed.draw(hud):
            winner = "undecided"
            pygame.mixer.Sound.play(blip)
            switch("page router")
        if backButton2.draw(hud):
            pygame.mixer.Sound.play(blip)
            switch("main")
    
    # This module redirects users to the next screen based on certain criteria.
    # All decision-making concerning which screen to use is done here in order to see where each screen goes with certain conditions.
    # Does not involve first few screens as they move in a more linear fashion, with the main menu as a pseudo-hub
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
            deselect_cd = 0
            StoredBoats = [1, 1, 1, 1, 1]
            turn = 0
            # reset vars for prompt screens
            prompt_cd = 60
            if selectedPlayerMode == False: #if 1 player mode was selected
                if playersReady == 0: #if no players have placed boats i.e if the player is about to place boats
                    P1Boats = []
                    playersReady = 1
                    switch("P1Prompt")
                elif playersReady == 1: #if the player has placed boats i.e AI is ready to prepare for game
                    P1Boats = PlacingGrid
                    P1Rot = BoatRotation
                    P2Boats = []
                    playersReady = 2
                    switch("AIPrep")
            else: #if 2 player mode was selected
                if playersReady == 0: #if no players have placed boats i.e if player 1 is about to place boats
                    P1Boats = []
                    playersReady = 1
                    switch("P1Prompt")
                elif playersReady == 1: #if only 1 player has placed boats i.e if player 2 is about to place boats
                    P1Boats = PlacingGrid
                    P1Rot = BoatRotation
                    P2Boats = []
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
            # check game ending conditions
            if turn != 0: #only do this once the first turn has passed
                # if in 1 Player and the player has run out of time
                if selectedPlayerMode == False and time_enabled == True and P1Time <= 0:
                    playerHitCount = 0
                    for sl in P2Boats:
                        for i in sl:
                            if i in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                playerHitCount += 1
                    botHitCount = 0
                    for sl in P1Boats:
                        for i in sl:
                            if i in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                botHitCount += 1
                    if botHitCount > playerHitCount:
                        loser = "Player 1"
                        if difficulty == "Easy":
                            winner = "AI (Easy)"
                            quote = random.choice(["They're in pieces.", "No one is walking away.", "Is that the best you've got?",
                                                  "I would let you live, but that does not compute.",  "Their crew got sloppy."])
                        else:
                            winner = "AI (Hard)"
                            quote = random.choice(["I could activate training mode if that's more your skill level.",
                                                  "I would let you live, but that does not compute.", "Go back to fighting bots.",
                                                  "I'm built different.", "I bet you've never seen a can opener do that.",
                                                  "In a fair fight I'd still beat you.", "It's not aimbot, it's a skill issue."])
                    else:
                        winner = "Player 1"
                        loser = "AI"
                        quote = random.choice(["The toaster is broken.", "Who's the old dog now?", "Not so tough after all.",
                                              "Robots don't belong in water.", "Someone missed a software update.", "Your circuits are fried."])
                # if in 2 Player and both players have run out of time
                if time_enabled == True and P1Time <= 0 and P2Time <= 0:
                    player1HitCount = 0
                    for sl in P2Boats:
                        for i in sl:
                            if i in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                player1HitCount += 1
                    player2HitCount = 0
                    for sl in P1Boats:
                        for i in sl:
                            if i in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                player2HitCount += 1
                    if player2HitCount > player1HitCount:
                        winner = "Player 2"
                        loser = "Player 1"
                        quote = random.choice(["Who's the old dog now?", "Not so tough after all.", "Sometimes you gotta get your hands dirty.",
                                          "That's why they put me in charge.", "There's some things you just can't teach.", "Like fish in a barrel."])
                    else:
                        winner = "Player 1"
                        loser = "Player 2"
                        quote = random.choice(["Who's the old dog now?", "Not so tough after all.", "Sometimes you gotta get your hands dirty.",
                                          "That's why they put me in charge.", "There's some things you just can't teach.", "Like fish in a barrel."])
                # if all boats of player 1 have been sunk
                if P1Boats_sunk == [1, 1, 1, 1, 1]:
                    loser = "Player 1"
                    if selectedPlayerMode == False:
                        if difficulty == "Easy":
                            winner = "AI (Easy)"
                            quote = random.choice(["They're in pieces.", "No one is walking away.", "Is that the best you've got?",
                                                  "I would let you live, but that does not compute.",  "Their crew got sloppy."])
                        else:
                            winner = "AI (Hard)"
                            quote = random.choice(["I could activate training mode if that's more your skill level.",
                                                  "I would let you live, but that does not compute.", "Go back to fighting bots.",
                                                  "I'm built different.", "I bet you've never seen a can opener do that.",
                                                  "In a fair fight I'd still beat you.", "It's not aimbot, it's a skill issue."])
                    else:
                        winner = "Player 2"
                        quote = random.choice(["Who's the old dog now?", "Not so tough after all.", "Sometimes you gotta get your hands dirty.",
                                          "That's why they put me in charge.", "There's some things you just can't teach.", "Like fish in a barrel."])
                # if all boats of player 2/AI have been sunk
                if P2Boats_sunk == [1, 1, 1, 1, 1]:
                    winner = "Player 1"
                    if selectedPlayerMode == False:
                        loser = "AI"
                        quote = random.choice(["The toaster is broken.", "Who's the old dog now?", "Not so tough after all.",
                                              "Robots don't belong in water.", "Someone missed a software update.", "Your circuits are fried."])
                    else:
                        loser = "Player 2"
                        quote = random.choice(["Who's the old dog now?", "Not so tough after all.", "Sometimes you gotta get your hands dirty.",
                                          "That's why they put me in charge.", "There's some things you just can't teach.", "Like fish in a barrel."])

            turn += 1 #on init turn is 0, first turn changes to 1
            # set anim vars
            mov_cd = 0
            nuke_anim = False
            nuke_anim2 = False
            nuke_ticks = 0
            rounded_nuke_ticks = 0
            door_anim = False
            door_ticks = 0
            if winner == "undecided": #if no winner currently (game still in progress)
                if turn == 1: #on first turn
                    # init game vars
                    selected_cell = pygame.Vector2(0,0)
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
                    P1Boats_sunk_visible = [0, 0, 0, 0, 0]
                    P2Boats_sunk_visible = [0, 0, 0, 0, 0]
                    Prev_action = []
                    Prev_action2 = []
                    if time_enabled:
                        P1Time = time_set
                        P2Time = time_set
                    x = 0
                    y = 0
                    target_cell = pygame.Vector2(0,0)
                    target_cell2 = pygame.Vector2(0,0)
                    AI_hit_reg = []
                    locked_on_ship = False
                    uncleared_cells = []
                    switch("P1Game")
                    door_anim = False
                    door_ticks = 0
                else:
                    if selectedPlayerMode == False: # one player mode
                        if turn % 2 == 1: #Player 1 takes odd turns
                            anim_ticks = 0
                            rounded_anim_ticks = 0
                            switch("P1Game")
                        else: #AI takes even turns
                            anim_ticks = 0
                            rounded_anim_ticks = 0
                            switch("AI Turn")
                    else: # two player mode
                        door_anim = True
                        if turn % 2 == 1: #Player 1 takes odd turns
                            if time_enabled == True: #if timed mode enabled
                                if P1Time > 0: #if timer still above 0
                                    anim_ticks = 0
                                    rounded_anim_ticks = 0
                                    switch("P1Switch")
                                else: #if ran out of time
                                    turn+=1
                                    door_anim = False
                                    nuke_ticks = 0
                                    rounded_nuke_ticks = 0
                                    switch("P2Game")
                            else: #if timed mode disabled
                                anim_ticks = 0
                                rounded_anim_ticks = 0
                                switch("P1Switch")
                        else: #Player 2 takes odd turns
                            if time_enabled == True: #if timed mode enabled
                                if P2Time > 0: #if timer still above 0
                                    anim_ticks = 0
                                    rounded_anim_ticks = 0
                                    switch("P2Switch")
                                else: #if ran out of time
                                    turn+=1
                                    door_anim = False
                                    nuke_ticks = 0
                                    rounded_nuke_ticks = 0
                                    switch("P1Game")
                            else: #if timed mode disabled
                                anim_ticks = 0
                                rounded_anim_ticks = 0
                                switch("P2Switch")
            else: #if someone has won the game
                # calculate win stats
                inGame = False
                door_ticks = 0
                door_anim = True

                quote = '"' + quote + '"'

                if winner == "Player 1":
                    checkGrid = copy.deepcopy(P2Boats)
                else:
                    checkGrid = copy.deepcopy(P1Boats)

                # battle report calculations
                shotCount = 0
                for sl in checkGrid:
                    for i in sl:
                        if i in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                            shotCount += 1
                # devtest game skips
                if shotCount == 0:
                    shotCount = 1
                accuracy = round(17*100/shotCount)
                turnCount = (turn-1)//2 + 1
                # devtest game skips
                if turnCount == 0:
                    turnCount = 1
                spt = round(shotCount/turnCount, 1)

                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                if winner == "AI (Easy)" or winner == "AI (Hard)":
                    pygame.mixer.music.load(resource_path("sounds/Music/Enemy Ship Approaching.ogg"))
                else:
                    pygame.mixer.music.load(resource_path("sounds/Music/restless sea.wav"))
                pygame.mixer.music.play()
                switch("win")
    
    if game_screen == "P1Prompt":
        if selectedPlayerMode == False:
            draw_text("Place down your ships", font1, (0, 0, 0), (1280-font1.size("Place down your ships")[0])/2, 100)
        else:
            draw_text("Pass this device to Player 1", font1, (0, 0, 0), (1280-font1.size("Pass this device to Player 1")[0])/2, 100)
        if prompt_cd <= 0:
            if promptProceed.draw(hud):
                pygame.mixer.Sound.play(blip)
                switch("boat placing")
        else:
            promptDisabled.draw(hud)
        prompt_cd -= 1  * 60 * dt

    elif game_screen == "P1Switch":
        draw_text("Pass this device to Player 1", font1, (0, 0, 0), (1280-font1.size("Pass this device to Player 1")[0])/2, 100)
        if promptProceed.draw(hud) and door_anim == False:
            pygame.mixer.Sound.play(blip)
            door_ticks = 0
            switch("P1Game")
        if door_anim == True:
            
            f = 2
            delay = 0
            if (door_ticks-delay) // f <= f*0:
                switch_door = widgets.Image(640, 360, blast_door_1, 1)
            elif (door_ticks-delay) // f == f*1:
                switch_door = widgets.Image(640, 360, blast_door_2, 1)
            elif (door_ticks-delay) // f == f*2:
                switch_door = widgets.Image(640, 360, blast_door_3, 1)
            elif (door_ticks-delay) // f == f*3:
                switch_door = widgets.Image(640, 360, blast_door_4, 1)
            elif (door_ticks-delay) // f == f*4:
                switch_door = widgets.Image(640, 360, blast_door_5, 1)
            elif (door_ticks-delay)// f == f*5:
                switch_door = widgets.Image(640, 360, blast_door_6, 1)
            elif (door_ticks-delay) // f == f*6:
                switch_door = widgets.Image(640, 360, blast_door_7, 1)
            elif (door_ticks-delay) // f == f*7:
                switch_door = widgets.Image(640, 360, blast_door_8, 1)
            
            if door_ticks > 30:
                door_anim = False
            
            switch_door.draw(hud)

            door_ticks += 1  * 60 * dt
    
    elif game_screen == "P2Prompt":
        draw_text("Pass this device to Player 2", font1, (0, 0, 0), (1280-font1.size("Pass this device to Player 2")[0])/2, 100)
        if prompt_cd <= 0:
            if promptProceed.draw(hud):
                pygame.mixer.Sound.play(blip)
                switch("boat placing")
        else:
            promptDisabled.draw(hud)
        prompt_cd -= 1  * 60 * dt
    
    elif game_screen == "P2Switch":
        draw_text("Pass this device to Player 2", font1, (0, 0, 0), (1280-font1.size("Pass this device to Player 2")[0])/2, 100)
        if promptProceed.draw(hud) and door_anim == False:
            pygame.mixer.Sound.play(blip)
            door_ticks = 0
            switch("P2Game")
        if door_anim == True:
            
            f = 2
            delay = 0
            if (door_ticks-delay) // f <= f*0:
                switch_door = widgets.Image(640, 360, blast_door_1, 1)
            elif (door_ticks-delay) // f == f*1:
                switch_door = widgets.Image(640, 360, blast_door_2, 1)
            elif (door_ticks-delay) // f == f*2:
                switch_door = widgets.Image(640, 360, blast_door_3, 1)
            elif (door_ticks-delay) // f == f*3:
                switch_door = widgets.Image(640, 360, blast_door_4, 1)
            elif (door_ticks-delay) // f == f*4:
                switch_door = widgets.Image(640, 360, blast_door_5, 1)
            elif (door_ticks-delay)// f == f*5:
                switch_door = widgets.Image(640, 360, blast_door_6, 1)
            elif (door_ticks-delay) // f == f*6:
                switch_door = widgets.Image(640, 360, blast_door_7, 1)
            elif (door_ticks-delay) // f == f*7:
                switch_door = widgets.Image(640, 360, blast_door_8, 1)
            
            if door_ticks > 30:
                door_anim = False
            
            switch_door.draw(hud)

            door_ticks += 1 * 60 * dt

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
            pygame.mixer.Sound.play(blip)
            inGame = True
            switch("page router")

    elif game_screen == "boat placing":
        screen.blit(metal_screen, (0, 0))
        hud.blit(left_Board_img, (0, 0))

        control_text = [
            "- Select Ships",
            "- Move Cursor",
            "- Move Quicker",
            "- Rotate Ship",
            "- Place Down Ship",
            "- Store Ship"
        ]

        k = 0
        for icon in [controls_numbers_img, controls_wasd_img, controls_shift_img, controls_r_img, controls_e_img, controls_f_img]:
            if k == 1:
                hud.blit(pygame.transform.scale_by(icon, (1.5, 1.5)), (50, 260+50-12))
            else:
                hud.blit(pygame.transform.scale_by(icon, (1.5, 1.5)), (50, 260+50*k))
            draw_text(f"{control_text[k]}", font4, (0, 0, 0), 200, 260-7+50*k)
            k += 1

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
                    if (keys[pygame.K_w] or keys[pygame.K_UP]) and selected_cell.y > 0:
                        selected_cell.y -= 1
                        mov_cd = 10
                    if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and selected_cell.y < 9:
                        selected_cell.y += 1
                        mov_cd = 10
                    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and selected_cell.x > 0:
                        selected_cell.x -= 1
                        mov_cd = 10
                    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and selected_cell.x < 9:
                        selected_cell.x += 1
                        mov_cd = 10
                
                if mov_cd > 7 and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
                    mov_cd = 7
                
                if deselect_cd <= 0 and keys[pygame.K_f]:
                    selected_boat = 5
                    selected_cell = pygame.Vector2(10, 10)
                    cur_boat_len = boat_len[selected_boat]
                    deselect_cd = 15
                            
                
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
        
        mov_cd -= 1 * 60 * dt
        rot_cd -= 1 * 60 * dt
        swap_cd -= 1 * 60 * dt
        stamp_cd -= 1 * 60 * dt
        deselect_cd -= 1 * 60 * dt

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
            pygame.mixer.Sound.play(blip)
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
                deselect_cd = 0
                StoredBoats = [0, 0, 0, 0, 0]

        if confirmFleet_button.draw(hud):
            if StoredBoats == [0, 0, 0, 0, 0]:
                pygame.mixer.Sound.play(blip)
                if messagebox.askokcancel("Confirm Boat Placement", "Your boats will be locked in place for the rest of the game.\nDo you wish to continue?"):
                    switch("page router")
            else:
                pygame.mixer.Sound.play(denyClick_sfx1)
    
    elif game_screen == "GameReady":
        draw_text("Start Game", font1, (0, 0, 0), (1280-font1.size("Start Game")[0])/2, 100)
        if gameBegin.draw(hud):
            pygame.mixer.Sound.play(blip)
            inGame = True
            switch("page router")

    elif game_screen == "In Game Menu":
        screen.blit(pygame.transform.scale(metal_screen, (1280, 720)), (0, 0))
        screen.blit(big_Board_img, (0, 0))

        if resume_button.draw(hud):
            pygame.mixer.Sound.play(blip)
            switch(return_screen)
        
        if option2_button.draw(hud):
            pygame.mixer.Sound.play(blip)
            switch("In Game Options")

        if leave_button.draw(hud):
            inGame = False
            pygame.mixer.Sound.play(blip)
            switch("main")


    elif game_screen == "In Game Options":
        screen.blit(pygame.transform.scale(metal_screen, (1280, 720)), (0, 0))
        screen.blit(big_Board_img, (0, 0))

        draw_text("Sound Options", font1, (0, 0, 0), (1280-font1.size("Sound Options")[0])/2, 50)

        if backButton.draw(hud):
            pygame.mixer.Sound.play(blip)
            switch("In Game Menu")
        
        draw_text("Master Volume", font3, (0, 0, 0), 100, 250)
        master_lvl = round(masterVolume.draw(hud), 2)
        draw_text(f"{master_lvl}", font3, (0, 0, 0), 1050, 250)
        if masterMute.draw(hud) == True:
            master_lvl = 0


        draw_text("Music Volume", font3, (0, 0, 0), 100, 375)
        music_lvl = round(musicVolume.draw(hud), 2)
        draw_text(f"{music_lvl}", font3, (0, 0, 0), 1050, 375)
        if musicMute.draw(hud) == True:
            music_lvl = 0

        pygame.mixer.music.set_volume(music_lvl*master_lvl)


        draw_text("SFX Volume", font3, (0, 0, 0), 100, 500)
        past_lvl = sfx_lvl
        sfx_lvl = round(sfxVolume.draw(hud), 2)
        draw_text(f"{sfx_lvl}", font3, (0, 0, 0), 1050, 500)
        if sfxMute.draw(hud) == True:
            sfx_lvl = 0
        
        if abs(sfx_lvl-past_lvl) > 0.05:
            door_open_sfx.set_volume(0.75)
            door_close_sfx.set_volume(0.75)
            startup_sfx1.set_volume(sfx_lvl*master_lvl)
            startup_sfx2.set_volume(sfx_lvl*master_lvl)
            blip.set_volume(sfx_lvl*master_lvl)
            widgets.changeBlip(sfx_lvl*master_lvl)
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
        

    elif game_screen == "AI Turn":
        screen.blit(metal_screen, (0, 0))

        if pause_button.draw(hud):
            pygame.mixer.Sound.play(blip)
            return_screen = "AI Turn"
            switch("In Game Menu")

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

        if selectedPlayerMode == False:
            leftRender.blit(computer_gridlabel, (160, 40))
        else:
            leftRender.blit(player2_gridlabel, (160, 40))
        rightRender.blit(player1_gridlabel, (160, 40))

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
            
        if selectedPlayerMode == False:
            if difficulty == "Easy":
                hud.blit(hud_P1A1_img, (0, 0))
            else:
                hud.blit(hud_P1A2_img, (0, 0))
        else:
            hud.blit(hud_P1P2_img, (0, 0))
        
        if time_enabled == True:
            hud.blit(hud_time_img, (0, 0))

            # Calculate minutes and seconds
            minutes = max(P1Time // 60, 0)  # Ensure minutes are not negative
            seconds = max(P1Time % 60, 0) # Ensure seconds are not negative
            
            timer_text = font3.render(f"{int(minutes):02d}:{int(seconds):02d}", True, (0, 0, 0))
            hud.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 3))

        keys = pygame.key.get_pressed()

        t = 60
        scale = 10
        diff = 45/t
        delay = 30
        if rounded_anim_ticks <= delay:
            left_size = screen.get_width()/2 + scale*(1 + (0.5*t)*diff)
            right_size = screen.get_width()/2 + scale*(1 - (0.5*t)*diff)
            left_pos = pygame.Vector2(55, 50-(left_size*0.13))
            right_pos = pygame.Vector2(1225-right_size, 670-(right_size*0.69))
            anim_ticks += 1*dbltime * 60 * dt
            rounded_anim_ticks = round(anim_ticks)
        elif delay < rounded_anim_ticks <= delay + t:
            left_size = screen.get_width()/2 + scale*(1 + (0.5*t - (rounded_anim_ticks - delay))*diff)
            right_size = screen.get_width()/2 + scale*(1 - (0.5*t - (rounded_anim_ticks - delay))*diff)
            left_pos = pygame.Vector2(55, 50-(left_size*0.13))
            right_pos = pygame.Vector2(1225-right_size, 670-(right_size*0.69))
            anim_ticks += 1*dbltime * 60 * dt
            rounded_anim_ticks = round(anim_ticks)
        else:
            if difficulty == "Easy":
                # merns algorithm
                while True:
                    decision = random.randint(0, 99)
                    if decision in AI_hit_reg: #if cell already hit, re-generate cell
                        pass
                    else:
                        AI_hit_reg.append(decision)
                        x = int(decision % 10)
                        y = int((decision - x) / 10)
                        P1Boats[y][x] += 5
                        Prev_action.append(decision)
                        if P1Boats[y][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                            # get another turn if hits a boat
                            pass
                        else:
                            switch("page router")
                            break
            elif difficulty == "Hard":
                if locked_on_ship == False: #ship not found
                    while True:
                        if len(uncleared_cells) > 0: #if a cell is still unresolved after sinking a ship, lock on that cell (if ships are bunched up)
                            locked_on_ship = True
                            lock_coords = pygame.Vector2(uncleared_cells[0]%10, (uncleared_cells[0]-(uncleared_cells[0]%10))/10)
                            OG_coords = pygame.Vector2(uncleared_cells[0]%10, (uncleared_cells[0]-(uncleared_cells[0]%10))/10)
                            check_dir = 1
                            found_dir = 0
                            double_check = 0
                            break
                        # unfairness multipler used to speed up games for dev testing, automatically knows the locaiton of a ship
                        # if the unfairness value is higher than the generated value, then trigger cheat (0 for disable, 10 for always unfair)
                        if unfairness_multiplier > random.randint(0, 9):
                            #generate cells until a ship is found
                            decision = random.randint(0, 99)
                            if decision in AI_hit_reg:
                                pass
                            else:
                                x = int(decision % 10)
                                y = int((decision - x) / 10)
                                # if boat hit, hit boat, else re-generate cell
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
                        else: #if cheat opportunity fails or is disabled
                            offset = random.randint(0, 1)
                            row = random.randint(0, 4)
                            column = random.randint(0, 4)
                            # generate cells in a checkboard pattern

                            true_row = 2*row + offset
                            true_column = 2*column + offset
                            true_loc = true_row*10+true_column
                            # translate generated cell to list index
                            if true_loc in AI_hit_reg: #if cell already hit, re-generate cell
                                pass
                            else: #if cell not hit, hit cell
                                AI_hit_reg.append(true_loc)
                                x = true_column
                                y = true_row
                                P1Boats[y][x] += 5
                                Prev_action.append(10*y+x)
                                # if boat hit, refund turn and lock on cell
                                if P1Boats[y][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    locked_on_ship = True
                                    lock_coords = pygame.Vector2(x, y)
                                    OG_coords = pygame.Vector2(x, y)
                                    check_dir = 1
                                    found_dir = 0
                                    double_check = 0
                                    uncleared_cells = [10*y+x]
                                    break
                                else: #if miss, end turn
                                    switch("page router")
                                    break
                if locked_on_ship == True: #ship found
                    x = int(lock_coords.x)
                    y = int(lock_coords.y)
                    # save lock coords
                    # when found_dir == 0, AI is still trying to find the orientation of the boat
                    # direction key:
                    # 1: up to the right
                    # 2: down to the right
                    # 3: down to the left
                    # 4: up to the left
                    if found_dir == 0:
                        while True:
                            if check_dir == 1:
                                # if cell in direction 1 is either off board or already hit
                                if y == 0 or P1Boats[y-1][x] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    check_dir = 2
                                    lock_coords = OG_coords
                                # else if cell is not already hit
                                elif not 10*(y-1)+x in AI_hit_reg:
                                    # try to hit the cell
                                    AI_hit_reg.append(10*(y-1)+x)
                                    P1Boats[y-1][x] += 5
                                    Prev_action.append(10*(y-1)+x)
                                    # if a ship is found, keep on hitting that direction
                                    if P1Boats[y-1][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                        found_dir = 1
                                        uncleared_cells.append(10*(y-1)+x)
                                        lock_coords = pygame.Vector2(x, y-1)
                                        break
                                    else: #if a ship not found, check next direction
                                        check_dir = 2
                                        lock_coords = OG_coords
                                        switch("page router")
                                        break
                                else: #if neither case passes, then check next direction (this should not trigger, but is there if system fails)
                                    check_dir = 2
                                    lock_coords = OG_coords
                            elif check_dir == 2: #follows same logic as first dir, except checks second dir
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
                            elif check_dir == 3: #follows same logic as first dir, except checks third dir
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
                            elif check_dir == 4: #follows similar logic as first dir, except checks fourth dir
                                if x == 0 or P1Boats[y][x-1] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    # this should not trigger, but just in case
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
                                        # this should not trigger, but just in case
                                        locked_on_ship = False
                                        switch("page router")
                                        break
                    else: #if orientation found
                        lock = True
                        while lock:
                            x = int(lock_coords.x)
                            y = int(lock_coords.y)
                            # save lock coords
                            # direction key:
                            # 1: up to the right
                            # 2: down to the right
                            # 3: down to the left
                            # 4: up to the left
                            if found_dir == 1:
                                if y == 0 or P1Boats[y-1][x] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                    # if next cell is off screen or already hit, backtrack and hit opposite direction
                                    found_dir = 3
                                    lock_coords = OG_coords
                                    double_check += 1
                                else: # try to hit cell
                                    AI_hit_reg.append(10*(y-1)+x)
                                    P1Boats[y-1][x] += 5
                                    Prev_action.append(10*(y-1)+x)
                                    # if boat hit, update lock coords and hit next
                                    if P1Boats[y-1][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                                        lock_coords = pygame.Vector2(x, y-1)
                                        uncleared_cells.append(10*(y-1)+x)
                                    else:
                                        # if miss, backtrack and hit opposite direction, end turn
                                        found_dir = 3
                                        lock_coords = OG_coords
                                        double_check += 1
                                        switch("page router")
                                        lock = False
                            elif found_dir == 2: #follows same logic as first dir, but checks second dir
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
                            elif found_dir == 3: #follows same logic as first dir, but checks third dir
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
                            elif found_dir == 4: #follows same logic as first dir, but checks fourth dir
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
                            # check if a boat has been sunk, if yes then release lockon ship
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
                            # resolve cells that have been sunk
                            for i in uncleared_cells:
                                cell = P1Boats[int((i-(i%10))/10)][int(i%10)]
                                if (cell in [15, 16] and P1Boats_sunk[0] == 1)\
                                     or (cell in [25, 26, 27] and P1Boats_sunk[1] == 1)\
                                     or (cell in [35, 36, 37] and P1Boats_sunk[2] == 1)\
                                     or (cell in [45, 46, 47, 48] and P1Boats_sunk[3] == 1)\
                                     or (cell in [55, 56, 57, 58, 59] and P1Boats_sunk[4] == 1):
                                    uncleared_cells.remove(i)
                            # if checked both directions and no ship sunk, unlock and resolve cases
                            if double_check == 2:
                                locked_on_ship = False
                                double_check = 0
                                lock = False

    elif game_screen == "P1Game":
        # render background and pause button
        screen.blit(metal_screen, (0, 0))

        if pause_button.draw(hud):
            pygame.mixer.Sound.play(blip)
            return_screen = "P1Game"
            switch("In Game Menu")

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
        
        # grab pressed keys
        keys = pygame.key.get_pressed()

        # devtesting, automatically lose/win by holding corresponding buttons
        if devmode == 1 and keys[pygame.K_l]:
            dev_sustain +=1 * 60 * dt
            if dev_sustain > 30:
                P1Boats_sunk = [1, 1, 1, 1, 1]
                switch("page router")
        elif not keys[pygame.K_p]:
            dev_sustain = 0

        if devmode == 1 and keys[pygame.K_p]:
            dev_sustain +=1 * 60 * dt
            if dev_sustain > 30:
                P2Boats_sunk = [1, 1, 1, 1, 1]
                switch("page router")
        elif not keys[pygame.K_l]:
            dev_sustain = 0
        
        # if move cooldown finished, and no animations are playing, move cursor. make sure that cursor does not go offscreen
        if mov_cd <= 0 and nuke_anim == False and destroyer_sink_anim == False and submarine_sink_anim == False\
            and cruiser_sink_anim == False and battleship_sink_anim == False and carrier_sink_anim == False:
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and selected_cell.y > 0:
                selected_cell.y -= 1
                mov_cd = 10
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and selected_cell.y < 9:
                selected_cell.y += 1
                mov_cd = 10
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and selected_cell.x > 0:
                selected_cell.x -= 1
                mov_cd = 10
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and selected_cell.x < 9:
                selected_cell.x += 1
                mov_cd = 10

        mov_cd -= 1 * 60 * dt # decrease move cooldown

        #if shift button pressed, then set cooldown to half normal value when above half normal value
        if mov_cd > 5 and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            mov_cd = 5

        # render grid labels
        if selectedPlayerMode == False:
            leftRender.blit(computer_gridlabel, (160, 40))
        else:
            leftRender.blit(player2_gridlabel, (160, 40))
        rightRender.blit(player1_gridlabel, (160, 40))

        # left render (Aaron Module)
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
                            if rounded_nuke_ticks > 30 and rounded_nuke_ticks <= 35:
                                y_level = 10+x*ydil+y*ydil-(rounded_nuke_ticks-30)*0.05
                            elif rounded_nuke_ticks > 35 and rounded_nuke_ticks <= 40:
                                y_level = 10+x*ydil+y*ydil-(40-rounded_nuke_ticks)*0.1
                            else:
                                not_cell = False
                        elif pygame.Vector2(x, y) == target_cell:
                            if rounded_nuke_ticks > 30 and rounded_nuke_ticks <= 40:
                                y_level = 10+x*ydil+y*ydil+(rounded_nuke_ticks-30)*0.3
                            else:
                                not_cell = False
                        else:
                            not_cell = False
                    elif (x in [target_cell.x-2, target_cell.x+2] and y in [target_cell.y-2, target_cell.y-1, target_cell.y, target_cell.y+1, target_cell.y+2]) or \
                    (y in [target_cell.y-2, target_cell.y+2] and x in [target_cell.x-1, target_cell.x, target_cell.x+1]):
                        if rounded_nuke_ticks > 35 and rounded_nuke_ticks <= 40:
                            y_level = 10+x*ydil+y*ydil-(rounded_nuke_ticks-35)*0.05
                        elif rounded_nuke_ticks > 40 and rounded_nuke_ticks <= 45:
                            y_level = 10+x*ydil+y*ydil-(45-rounded_nuke_ticks)*0.1
                        else:
                            not_cell = False
                    elif (x in [target_cell.x-3, target_cell.x+3] and y in [target_cell.y-3, target_cell.y-2, target_cell.y-1, target_cell.y, target_cell.y+1, target_cell.y+2, target_cell.y+3]) or \
                    (y in [target_cell.y-3, target_cell.y+3] and x in [target_cell.x-2, target_cell.x-1, target_cell.x, target_cell.x+1, target_cell.x+2]):
                        if rounded_nuke_ticks > 40 and rounded_nuke_ticks <= 45:
                            y_level = 10+x*ydil+y*ydil-(rounded_nuke_ticks-40)*0.05
                        elif rounded_nuke_ticks > 45 and rounded_nuke_ticks <= 50:
                            y_level = 10+x*ydil+y*ydil-(50-rounded_nuke_ticks)*0.1
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

        # right render (Aaron Module)
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
                        if ((P1Boats_sunk_visible[0] == 1 and tile in [15, 16]) or (P1Boats_sunk_visible[1] == 1 and tile in [25, 26, 27])\
                            or (P1Boats_sunk_visible[2] == 1 and tile in [35, 36, 37])\
                            or (P1Boats_sunk_visible[3] == 1 and tile in [45, 46, 47, 48])\
                            or (P1Boats_sunk_visible[4] == 1 and tile in [55, 56, 57, 58, 59])):
                            tile_sprite = hit_tiles.get(tile)
                else:
                    tile_sprite = funcs.get(tile, funcs.get(tile-5, "blank"))

                if tile_sprite == "blank":
                    pass
                elif nuke_anim2 == True:
                    not_cell = True
                    if (x in [target_cell.x-1, target_cell.x, target_cell.x+1]) and (y in [target_cell.y-1, target_cell.y, target_cell.y+1]):
                        if pygame.Vector2(x, y) != target_cell:
                            if rounded_anim_ticks > 30 and rounded_anim_ticks <= 35:
                                y_level = 10+x*ydil+y*ydil-(rounded_anim_ticks-30)*0.05
                            elif rounded_anim_ticks > 35 and rounded_anim_ticks <= 40:
                                y_level = 10+x*ydil+y*ydil-(40-rounded_anim_ticks)*0.1
                            else:
                                not_cell = False
                        elif pygame.Vector2(x, y) == target_cell:
                            if rounded_anim_ticks > 30 and rounded_anim_ticks <= 40:
                                y_level = 10+x*ydil+y*ydil+(rounded_anim_ticks-30)*0.3
                            else:
                                not_cell = False
                        else:
                            not_cell = False
                    elif (x in [target_cell.x-2, target_cell.x+2] and y in [target_cell.y-2, target_cell.y-1, target_cell.y, target_cell.y+1, target_cell.y+2]) or \
                    (y in [target_cell.y-2, target_cell.y+2] and x in [target_cell.x-1, target_cell.x, target_cell.x+1]):
                        if rounded_anim_ticks > 35 and rounded_anim_ticks <= 40:
                            y_level = 10+x*ydil+y*ydil-(rounded_anim_ticks-35)*0.05
                        elif rounded_anim_ticks > 40 and rounded_anim_ticks <= 45:
                            y_level = 10+x*ydil+y*ydil-(45-rounded_anim_ticks)*0.1
                        else:
                            not_cell = False
                    elif (x in [target_cell.x-3, target_cell.x+3] and y in [target_cell.y-3, target_cell.y-2, target_cell.y-1, target_cell.y, target_cell.y+1, target_cell.y+2, target_cell.y+3]) or \
                    (y in [target_cell.y-3, target_cell.y+3] and x in [target_cell.x-2, target_cell.x-1, target_cell.x, target_cell.x+1, target_cell.x+2]):
                        if rounded_anim_ticks > 40 and rounded_anim_ticks <= 45:
                            y_level = 10+x*ydil+y*ydil-(rounded_anim_ticks-40)*0.05
                        elif rounded_anim_ticks > 45 and rounded_anim_ticks <= 50:
                            y_level = 10+x*ydil+y*ydil-(50-rounded_anim_ticks)*0.1
                        else:
                            not_cell = False
                    else:
                        not_cell = False

                    if not_cell == False:
                        if rotate_cell == False:
                            rightRender.blit(tile_sprite, (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
                        else:
                            rightRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
                    else:
                        if rotate_cell == False:
                            rightRender.blit(tile_sprite, (144+x*xdil-y*xdil, y_level))
                        else:
                            rightRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, y_level))
                elif rotate_cell == False:
                    rightRender.blit(tile_sprite, (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
                else:
                    rightRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
        
        # animation constants (Aaron)
        t = 60
        scale = 10
        diff = 45/t
        if nuke_anim2 == False:
            delay = 110
        else:
            delay = 90
        if rounded_anim_ticks <= delay: #static, focus right grid
            if turn != 1 and nuke_anim2 == False:
                hud.blit(turn_banner_Opp, (0, 0))
            left_size = screen.get_width()/2 + scale*(1 - (0.5*t)*diff)
            right_size = screen.get_width()/2 + scale*(1 + (0.5*t)*diff)
            left_pos = pygame.Vector2(55, 50-(left_size*0.13))
            right_pos = pygame.Vector2(1225-right_size, 670-(right_size*0.69))
            anim_ticks += 1*dbltime * 60 * dt
            rounded_anim_ticks = round(anim_ticks)
            # animation nukes on right grid
            if nuke_anim2 == True:
                j = int(target_cell.y)
                i = int(target_cell.x)
                if rounded_anim_ticks <= 30:
                    rightOverlay.blit(pygame.transform.scale_by(nuke_img, (0.4, 0.4)), (144+i*xdil-j*xdil+2, (37+i*ydil+j*ydil) - 5*(30-rounded_anim_ticks)))
                if P1Boats[j][i] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    if rounded_anim_ticks >= 31 and pre_turn_sounds[0] == 0:
                        sound_list = [
                            explosion_sfx1, explosion_sfx2, explosion_sfx3, explosion_sfx4
                        ]
                        pygame.mixer.Sound.play(sound_list[random.randint(0, 3)])
                        pre_turn_sounds[0] = 1
                    if rounded_anim_ticks in range(31, 78):
                        if rounded_anim_ticks in range(31, 33):
                            explosion_img = explosion_frame_1
                        elif rounded_anim_ticks in range(33, 35):
                            explosion_img = explosion_frame_2
                        elif rounded_anim_ticks in range(35, 37):
                            explosion_img = explosion_frame_3
                        elif rounded_anim_ticks in range(37, 41):
                            explosion_img = explosion_frame_4
                        elif rounded_anim_ticks in range(41, 45):
                            explosion_img = explosion_frame_5
                        elif rounded_anim_ticks in range(45, 49):
                            explosion_img = explosion_frame_6
                        elif rounded_anim_ticks in range(53, 57):
                            explosion_img = explosion_frame_7
                        elif rounded_anim_ticks in range(57, 61):
                            explosion_img = explosion_frame_8
                        elif rounded_anim_ticks in range(61, 65):
                            explosion_img = explosion_frame_9
                        elif rounded_anim_ticks in range(65, 69):
                            explosion_img = explosion_frame_10
                        elif rounded_anim_ticks in range(69, 73):
                            explosion_img = explosion_frame_11
                        elif rounded_anim_ticks in range(73, 77):
                            explosion_img = explosion_frame_12
                        rightOverlay.blit(pygame.transform.scale_by(explosion_img, (1, 1)), (126+i*xdil-j*xdil+2, 37+i*ydil+j*ydil))
                else:
                    if rounded_anim_ticks >= 31 and pre_turn_sounds[0] == 0:
                        sound_list = [
                            splash_sfx1, splash_sfx2, splash_sfx3, splash_sfx4, splash_sfx5
                        ]
                        pygame.mixer.Sound.play(sound_list[random.randint(0, 4)])
                        pre_turn_sounds[0] = 1
                    if rounded_anim_ticks in range(31, 68):
                        if rounded_anim_ticks in range(31, 34):
                            splash_img = splash_frame_1
                        elif rounded_anim_ticks in range(34, 37):
                            splash_img = splash_frame_2
                        elif rounded_anim_ticks in range(37, 40):
                            splash_img = splash_frame_3
                        elif rounded_anim_ticks in range(40, 43):
                            splash_img = splash_frame_4
                        elif rounded_anim_ticks in range(43, 46):
                            splash_img = splash_frame_5
                        elif rounded_anim_ticks in range(46, 49):
                            splash_img = splash_frame_6
                        elif rounded_anim_ticks in range(49, 52):
                            splash_img = splash_frame_7
                        elif rounded_anim_ticks in range(52, 55):
                            splash_img = splash_frame_8
                        elif rounded_anim_ticks in range(55, 58):
                            splash_img = splash_frame_9
                        elif rounded_anim_ticks in range(58, 61):
                            splash_img = splash_frame_10
                        elif rounded_anim_ticks in range(61, 64):
                            splash_img = splash_frame_11
                        elif rounded_anim_ticks in range(64, 67):
                            splash_img = splash_frame_12
                        rightOverlay.blit(pygame.transform.scale_by(splash_img, (0.75, 0.75)), (134+i*xdil-j*xdil+2, 37+i*ydil+j*ydil))

        elif delay < rounded_anim_ticks <= delay + t:
            # check that there are not more actions to display (Aaron)
            if Prev_action != [] and nuke_anim2 == True:
                Prev_action.pop(0) #remove action once displayed (Aaron)
            if Prev_action != []:
                #show action if available (Aaron)
                x = int(Prev_action[0] % 10)
                y = int((Prev_action[0]-x)/10)
                target_cell = pygame.Vector2(x, y)
                nuke_anim2 = True
                pre_turn_sounds = [0]
                anim_ticks = 0
                rounded_anim_ticks = 0
            else: #if all actions displayed, move to player turn
                # shown sunken boats (Aaron)
                if P1Boats_sunk[0] == 1 and P1Boats_sunk_visible[0] == 0:
                    P1Boats_sunk_visible[0] = 1
                elif P1Boats_sunk[1] == 1 and P1Boats_sunk_visible[1] == 0:
                    P1Boats_sunk_visible[1] = 1
                elif P1Boats_sunk[2] == 1 and P1Boats_sunk_visible[2] == 0:
                    P1Boats_sunk_visible[2] = 1
                elif P1Boats_sunk[3] == 1 and P1Boats_sunk_visible[3] == 0:
                    P1Boats_sunk_visible[3] = 1
                elif P1Boats_sunk[4] == 1 and P1Boats_sunk_visible[4] == 0:
                    P1Boats_sunk_visible[4] = 1
                # if Player 1 lost in 1 player mode
                if selectedPlayerMode == False and door_anim == False and P1Boats_sunk_visible == [1, 1, 1, 1, 1]:
                    door_anim = True
                    door_sounds = [0]
                    door_ticks = 0
                # change grid sizes, move to left grid focus (Aaron)
                hud.blit(turn_banner_You, (0, 0))
                nuke_anim2 = False
                left_size = screen.get_width()/2 + scale*(1 - (0.5*t - (rounded_anim_ticks - delay))*diff)
                right_size = screen.get_width()/2 + scale*(1 + (0.5*t - (rounded_anim_ticks - delay))*diff)
                left_pos = pygame.Vector2(55, 50-(left_size*0.13))
                right_pos = pygame.Vector2(1225-right_size, 670-(right_size*0.69))
                anim_ticks += 1*dbltime * 60 * dt
                rounded_anim_ticks = round(anim_ticks)
        else: #player action phase
            # if no animations playing
            if nuke_anim == False and destroyer_sink_anim == False and submarine_sink_anim == False\
                and cruiser_sink_anim == False and battleship_sink_anim == False and carrier_sink_anim == False:
                # render cursor
                x = selected_cell.x
                y = selected_cell.y
                if P2Boats[int(selected_cell.y)][int(selected_cell.x)] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    leftOverlay.blit(cursorX, (144+x*xdil-y*xdil, -13+x*ydil+y*ydil))
                else:
                    leftOverlay.blit(cursorC, (144+x*xdil-y*xdil, -13+x*ydil+y*ydil))
                if door_anim == False and (P2Boats_sunk == [1, 1, 1, 1, 1] or (time_enabled == True and P1Time <= 0)):
                    # check if end game conditions met (if all Player 2 boats sunk or ran out of time)
                    door_anim = True
                    door_sounds = [0]
                    door_ticks = 0
            # if player tries to fire nuke (only when no animations playing)
            if (keys[pygame.K_SPACE] or keys[pygame.K_e]) and nuke_anim == False and destroyer_sink_anim == False and submarine_sink_anim == False\
                and cruiser_sink_anim == False and battleship_sink_anim == False and carrier_sink_anim == False:
                #if player tries to hit an already hit cell
                if P2Boats[int(selected_cell.y)][int(selected_cell.x)] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    pass 
                else: #if player tries to hit an untouched cell
                    # start nuke animation (Aaron) (cell ID change handled below)
                    nuke_anim = True
                    nuke_ticks = 0
                    rounded_nuke_ticks = 0
                    sink_anim_ticks = 0
                    nuke_sounds = [0]
                    # append animation for player 2 (Aaron)
                    Prev_action2.append(selected_cell.y*10 + selected_cell.x)

            if nuke_anim == True: #when nuke animation is playing
                # save targeted coords
                x = int(selected_cell.x)
                y = int(selected_cell.y)
                target_cell = pygame.Vector2(x, y)
                # play animations and sounds (Aaron)
                if rounded_nuke_ticks <= 30:
                    leftOverlay.blit(pygame.transform.scale_by(nuke_img, (0.4, 0.4)), (144+x*xdil-y*xdil+2, (-13+x*ydil+y*ydil) - 5*(30-rounded_nuke_ticks)))
                if P2Boats[y][x] in [10, 11, 20, 21, 22, 30, 31, 32, 40, 41, 42, 43, 50, 51, 52, 53, 54]:
                    if rounded_nuke_ticks >= 31 and nuke_sounds[0] == 0:
                        sound_list = [
                            explosion_sfx1, explosion_sfx2, explosion_sfx3, explosion_sfx4
                        ]
                        pygame.mixer.Sound.play(sound_list[random.randint(0, 3)])
                        nuke_sounds[0] = 1
                    if rounded_nuke_ticks in range(31, 78):
                        if rounded_nuke_ticks in range(31, 33):
                            explosion_img = explosion_frame_1
                        elif rounded_nuke_ticks in range(33, 35):
                            explosion_img = explosion_frame_2
                        elif rounded_nuke_ticks in range(35, 37):
                            explosion_img = explosion_frame_3
                        elif rounded_nuke_ticks in range(37, 41):
                            explosion_img = explosion_frame_4
                        elif rounded_nuke_ticks in range(41, 45):
                            explosion_img = explosion_frame_5
                        elif rounded_nuke_ticks in range(45, 49):
                            explosion_img = explosion_frame_6
                        elif rounded_nuke_ticks in range(53, 57):
                            explosion_img = explosion_frame_7
                        elif rounded_nuke_ticks in range(57, 61):
                            explosion_img = explosion_frame_8
                        elif rounded_nuke_ticks in range(61, 65):
                            explosion_img = explosion_frame_9
                        elif rounded_nuke_ticks in range(65, 69):
                            explosion_img = explosion_frame_10
                        elif rounded_nuke_ticks in range(69, 73):
                            explosion_img = explosion_frame_11
                        elif rounded_nuke_ticks in range(73, 77):
                            explosion_img = explosion_frame_12
                        leftOverlay.blit(pygame.transform.scale_by(explosion_img, (1, 1)), (126+x*xdil-y*xdil+2, -10+x*ydil+y*ydil))
                else:
                    if rounded_nuke_ticks >= 31 and nuke_sounds[0] == 0:
                        sound_list = [
                            splash_sfx1, splash_sfx2, splash_sfx3, splash_sfx4, splash_sfx5
                        ]
                        pygame.mixer.Sound.play(sound_list[random.randint(0, 4)])
                        nuke_sounds[0] = 1
                    if rounded_nuke_ticks in range(31, 68):
                        if rounded_nuke_ticks in range(31, 34):
                            splash_img = splash_frame_1
                        elif rounded_nuke_ticks in range(34, 37):
                            splash_img = splash_frame_2
                        elif rounded_nuke_ticks in range(37, 40):
                            splash_img = splash_frame_3
                        elif rounded_nuke_ticks in range(40, 43):
                            splash_img = splash_frame_4
                        elif rounded_nuke_ticks in range(43, 46):
                            splash_img = splash_frame_5
                        elif rounded_nuke_ticks in range(46, 49):
                            splash_img = splash_frame_6
                        elif rounded_nuke_ticks in range(49, 52):
                            splash_img = splash_frame_7
                        elif rounded_nuke_ticks in range(52, 55):
                            splash_img = splash_frame_8
                        if rounded_nuke_ticks in range(55, 58):
                            splash_img = splash_frame_9
                        elif rounded_nuke_ticks in range(58, 61):
                            splash_img = splash_frame_10
                        elif rounded_nuke_ticks in range(61, 64):
                            splash_img = splash_frame_11
                        elif rounded_nuke_ticks in range(64, 67):
                            splash_img = splash_frame_12
                        leftOverlay.blit(pygame.transform.scale_by(splash_img, (0.75, 0.75)), (134+x*xdil-y*xdil+2, -12+x*ydil+y*ydil))

                # update anim tick (Aaron)
                nuke_ticks += 1*dbltime * 60 * dt
                rounded_nuke_ticks = round(nuke_ticks)

                # when animation finished, handle events
                if rounded_nuke_ticks > 120:
                    # hit cell
                    P2Boats[y][x] += 5
                    # end animation
                    nuke_anim = False
                    # check for sunken boats, record info and play sink animation
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
                    # refund turn on hit else end turn
                    if P2Boats[y][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                        pass
                    else:
                        Prev_action = []
                        if selectedPlayerMode == True: #two player
                            if time_enabled == True and P2Time <= 0: #if Player two has run out of time, switch to page router to register turn, then come back
                                switch("page router")
                            else: #play door anim, then switch to page router
                                door_anim = True
                                door_sounds = [0]
                        else:
                            # switch to page router, then AI turn
                            switch("page router")

            # play sinking animations (Aaron)
            if destroyer_sink_anim == True:
                sink_anim_ticks += 1*dbltime * 60 * dt
                
                if sink_anim_ticks == 1*dbltime * 60 * dt:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                sink_anim_ticks = round(sink_anim_ticks)

                if sink_anim_ticks > 120:
                    destroyer_sink_anim = False
            
            if submarine_sink_anim == True:
                sink_anim_ticks += 1*dbltime * 60 * dt
                
                if sink_anim_ticks == 1*dbltime * 60 * dt:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                sink_anim_ticks = round(sink_anim_ticks)

                if sink_anim_ticks > 120:
                    submarine_sink_anim = False

            if cruiser_sink_anim == True:
                sink_anim_ticks += 1*dbltime * 60 * dt
                
                if sink_anim_ticks == 1*dbltime * 60 * dt:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                sink_anim_ticks = round(sink_anim_ticks)

                if sink_anim_ticks > 120:
                    cruiser_sink_anim = False
            
            if battleship_sink_anim == True:
                sink_anim_ticks += 1*dbltime * 60 * dt
                
                if sink_anim_ticks == 1*dbltime * 60 * dt:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                sink_anim_ticks = round(sink_anim_ticks)

                if sink_anim_ticks > 120:
                    battleship_sink_anim = False
            
            if carrier_sink_anim == True:
                sink_anim_ticks += 1*dbltime * 60 * dt
                
                if sink_anim_ticks == 1*dbltime * 60 * dt:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                sink_anim_ticks = round(sink_anim_ticks)

                if sink_anim_ticks > 120:
                    carrier_sink_anim = False

        # render hud (Aaron)
        if selectedPlayerMode == False:
            if difficulty == "Easy":
                hud.blit(hud_P1A1_img, (0, 0))
            else:
                hud.blit(hud_P1A2_img, (0, 0))
        else:
            hud.blit(hud_P1P2_img, (0, 0))
        
        # when timed mode is on (Gokul)
        if time_enabled == True:
            hud.blit(hud_time_img, (0, 0))

            if door_anim == False and nuke_anim == False and nuke_anim2 == False and rounded_anim_ticks > delay + t:
                P1Time -= dt  # Subtract time since last frame, only do this when no animations are playing (except for sinks)

            # Calculate minutes and seconds
            minutes = max(P1Time // 60, 0)  # Ensure minutes are not negative
            seconds = max(P1Time % 60, 0) # Ensure seconds are not negative
            
            timer_text = font3.render(f"{int(minutes):02d}:{int(seconds):02d}", True, (0, 0, 0))
            hud.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 3))
        
        # control icons (Aaron)
        control_text = [
            "-Move Cursor",
            "-Move Quicker",
            "",
            "-Fire"
        ]

        k = 0
        for icon in [controls_wasd_img, controls_shift_img, controls_space_img, controls_e_img]:
            if k == 0:
                hud.blit(pygame.transform.scale_by(icon, (1.2, 1.2)), (500, 655))
            elif k == 3:
                hud.blit(pygame.transform.scale_by(icon, (1.5, 1.5)), (520+120*2+45, 668))
            else:
                hud.blit(pygame.transform.scale_by(icon, (1.5, 1.5)), (520+120*k, 668))
            if k == 3:
                draw_text(f"{control_text[k]}", font5, (0, 0, 0), 530+130*2, 690)
            else:
                draw_text(f"{control_text[k]}", font5, (0, 0, 0), 530+130*k, 690)
            k += 1

        # door animation (Aaron)
        if door_anim == True:
            
            f = 2
            delay = 10
            if (door_ticks-delay) // f == f*0:
                switch_door = widgets.Image(640, 360, blast_door_8, 1)
            elif (door_ticks-delay) // f == f*1:
                switch_door = widgets.Image(640, 360, blast_door_7, 1)
            elif (door_ticks-delay) // f == f*2:
                switch_door = widgets.Image(640, 360, blast_door_6, 1)
            elif (door_ticks-delay) // f == f*3:
                switch_door = widgets.Image(640, 360, blast_door_5, 1)
            elif (door_ticks-delay) // f == f*4:
                switch_door = widgets.Image(640, 360, blast_door_4, 1)
            elif (door_ticks-delay)// f == f*5:
                switch_door = widgets.Image(640, 360, blast_door_3, 1)
            elif (door_ticks-delay) // f == f*6:
                switch_door = widgets.Image(640, 360, blast_door_2, 1)
            elif (door_ticks-delay) // f == f*7:
                switch_door = widgets.Image(640, 360, blast_door_1, 1)
            
            if door_ticks > delay:
                switch_door.draw(hud)

            if door_ticks >= 1 and door_sounds[0] == 0:
                pygame.mixer.Sound.play(door_close_sfx)
                door_sounds[0] = 1

            if door_ticks > 30:
                door_anim = False
                switch("page router")

            door_ticks += 1 * 60 * dt
    
    elif game_screen == "P2Game":

        screen.blit(metal_screen, (0, 0))

        if pause_button.draw(hud):
            pygame.mixer.Sound.play(blip)
            return_screen = "P2Game"
            switch("In Game Menu")

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
        
        
        keys = pygame.key.get_pressed()
        
        if mov_cd <= 0 and nuke_anim == False and destroyer_sink_anim == False and submarine_sink_anim == False\
            and cruiser_sink_anim == False and battleship_sink_anim == False and carrier_sink_anim == False:
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and selected_cell.y > 0:
                selected_cell.y -= 1
                mov_cd = 10
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and selected_cell.y < 9:
                selected_cell.y += 1
                mov_cd = 10
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and selected_cell.x > 0:
                selected_cell.x -= 1
                mov_cd = 10
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and selected_cell.x < 9:
                selected_cell.x += 1
                mov_cd = 10

        mov_cd -= 1 * 60 * dt

        if mov_cd > 5 and (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
            mov_cd = 5

        leftRender.blit(player1_gridlabel, (160, 40))
        rightRender.blit(player2_gridlabel, (160, 40))

        # left render
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
                    if (P1Boats_sunk[0] == 1 and tile in [15, 16]) or (P1Boats_sunk[1] == 1 and tile in [25, 26, 27])\
                        or (P1Boats_sunk[2] == 1 and tile in [35, 36, 37]) or (P1Boats_sunk[3] == 1 and tile in [45, 46, 47, 48])\
                        or (P1Boats_sunk[4] == 1 and tile in [55, 56, 57, 58, 59]):
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
                            if rounded_nuke_ticks > 30 and rounded_nuke_ticks <= 35:
                                y_level = 10+x*ydil+y*ydil-(rounded_nuke_ticks-30)*0.05
                            elif rounded_nuke_ticks > 35 and rounded_nuke_ticks <= 40:
                                y_level = 10+x*ydil+y*ydil-(40-rounded_nuke_ticks)*0.1
                            else:
                                not_cell = False
                        elif pygame.Vector2(x, y) == target_cell:
                            if rounded_nuke_ticks > 30 and rounded_nuke_ticks <= 40:
                                y_level = 10+x*ydil+y*ydil+(rounded_nuke_ticks-30)*0.3
                            else:
                                not_cell = False
                        else:
                            not_cell = False
                    elif (x in [target_cell.x-2, target_cell.x+2] and y in [target_cell.y-2, target_cell.y-1, target_cell.y, target_cell.y+1, target_cell.y+2]) or \
                    (y in [target_cell.y-2, target_cell.y+2] and x in [target_cell.x-1, target_cell.x, target_cell.x+1]):
                        if rounded_nuke_ticks > 35 and rounded_nuke_ticks <= 40:
                            y_level = 10+x*ydil+y*ydil-(rounded_nuke_ticks-35)*0.05
                        elif rounded_nuke_ticks > 40 and rounded_nuke_ticks <= 45:
                            y_level = 10+x*ydil+y*ydil-(45-rounded_nuke_ticks)*0.1
                        else:
                            not_cell = False
                    elif (x in [target_cell.x-3, target_cell.x+3] and y in [target_cell.y-3, target_cell.y-2, target_cell.y-1, target_cell.y, target_cell.y+1, target_cell.y+2, target_cell.y+3]) or \
                    (y in [target_cell.y-3, target_cell.y+3] and x in [target_cell.x-2, target_cell.x-1, target_cell.x, target_cell.x+1, target_cell.x+2]):
                        if rounded_nuke_ticks > 40 and rounded_nuke_ticks <= 45:
                            y_level = 10+x*ydil+y*ydil-(rounded_nuke_ticks-40)*0.05
                        elif rounded_nuke_ticks > 45 and rounded_nuke_ticks <= 50:
                            y_level = 10+x*ydil+y*ydil-(50-rounded_nuke_ticks)*0.1
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
                
                if tile == 5:
                    if Prev_action2 != []:
                        in_prev = False
                        for i in Prev_action2:
                            if int((i - (i%10))/10) == y and int(i%10) == x:
                                tile_sprite = funcs.get(tile-5, "blank")
                                in_prev = True
                        if in_prev == False:
                            tile_sprite = d_sea_nohit_tile
                    else:
                        tile_sprite = d_sea_nohit_tile
                elif tile in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    in_prev = False
                    if Prev_action2 != []:
                        for i in Prev_action2:
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
                        if ((P2Boats_sunk_visible[0] == 1 and tile in [15, 16]) or (P2Boats_sunk_visible[1] == 1 and tile in [25, 26, 27])\
                            or (P2Boats_sunk_visible[2] == 1 and tile in [35, 36, 37])\
                            or (P2Boats_sunk_visible[3] == 1 and tile in [45, 46, 47, 48])\
                            or (P2Boats_sunk_visible[4] == 1 and tile in [55, 56, 57, 58, 59])):
                            tile_sprite = hit_tiles.get(tile)
                else:
                    tile_sprite = funcs.get(tile, funcs.get(tile-5, "blank"))

                if tile_sprite == "blank":
                    pass
                elif nuke_anim2 == True:
                    not_cell = True
                    if (x in [target_cell.x-1, target_cell.x, target_cell.x+1]) and (y in [target_cell.y-1, target_cell.y, target_cell.y+1]):
                        if pygame.Vector2(x, y) != target_cell:
                            if rounded_anim_ticks > 30 and rounded_anim_ticks <= 35:
                                y_level = 10+x*ydil+y*ydil-(rounded_anim_ticks-30)*0.05
                            elif rounded_anim_ticks > 35 and rounded_anim_ticks <= 40:
                                y_level = 10+x*ydil+y*ydil-(40-rounded_anim_ticks)*0.1
                            else:
                                not_cell = False
                        elif pygame.Vector2(x, y) == target_cell:
                            if rounded_anim_ticks > 30 and rounded_anim_ticks <= 40:
                                y_level = 10+x*ydil+y*ydil+(rounded_anim_ticks-30)*0.3
                            else:
                                not_cell = False
                        else:
                            not_cell = False
                    elif (x in [target_cell.x-2, target_cell.x+2] and y in [target_cell.y-2, target_cell.y-1, target_cell.y, target_cell.y+1, target_cell.y+2]) or \
                    (y in [target_cell.y-2, target_cell.y+2] and x in [target_cell.x-1, target_cell.x, target_cell.x+1]):
                        if rounded_anim_ticks > 35 and rounded_anim_ticks <= 40:
                            y_level = 10+x*ydil+y*ydil-(rounded_anim_ticks-35)*0.05
                        elif rounded_anim_ticks > 40 and rounded_anim_ticks <= 45:
                            y_level = 10+x*ydil+y*ydil-(45-rounded_anim_ticks)*0.1
                        else:
                            not_cell = False
                    elif (x in [target_cell.x-3, target_cell.x+3] and y in [target_cell.y-3, target_cell.y-2, target_cell.y-1, target_cell.y, target_cell.y+1, target_cell.y+2, target_cell.y+3]) or \
                    (y in [target_cell.y-3, target_cell.y+3] and x in [target_cell.x-2, target_cell.x-1, target_cell.x, target_cell.x+1, target_cell.x+2]):
                        if rounded_anim_ticks > 40 and rounded_anim_ticks <= 45:
                            y_level = 10+x*ydil+y*ydil-(rounded_anim_ticks-40)*0.05
                        elif rounded_anim_ticks > 45 and rounded_anim_ticks <= 50:
                            y_level = 10+x*ydil+y*ydil-(50-rounded_anim_ticks)*0.1
                        else:
                            not_cell = False
                    else:
                        not_cell = False

                    if not_cell == False:
                        if rotate_cell == False:
                            rightRender.blit(tile_sprite, (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
                        else:
                            rightRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
                    else:
                        if rotate_cell == False:
                            rightRender.blit(tile_sprite, (144+x*xdil-y*xdil, y_level))
                        else:
                            rightRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, y_level))
                elif rotate_cell == False:
                    rightRender.blit(tile_sprite, (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
                else:
                    rightRender.blit(pygame.transform.flip(tile_sprite, True, False), (144+x*xdil-y*xdil, 10+x*ydil+y*ydil))
        
        t = 60
        scale = 10
        diff = 45/t
        if nuke_anim2 == False:
            delay = 110
        else:
            delay = 90
        if rounded_anim_ticks <= delay:
            if turn != 1 and nuke_anim2 == False:
                hud.blit(turn_banner_Opp, (0, 0))
            left_size = screen.get_width()/2 + scale*(1 - (0.5*t)*diff)
            right_size = screen.get_width()/2 + scale*(1 + (0.5*t)*diff)
            left_pos = pygame.Vector2(55, 50-(left_size*0.13))
            right_pos = pygame.Vector2(1225-right_size, 670-(right_size*0.69))
            anim_ticks += 1*dbltime * 60 * dt
            rounded_anim_ticks = round(anim_ticks)
            if nuke_anim2 == True:
                j = int(target_cell.y)
                i = int(target_cell.x)
                if rounded_anim_ticks <= 30:
                    rightOverlay.blit(pygame.transform.scale_by(nuke_img, (0.4, 0.4)), (144+i*xdil-j*xdil+2, (37+i*ydil+j*ydil) - 5*(30-rounded_anim_ticks)))
                if P2Boats[j][i] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    if rounded_anim_ticks >= 31 and pre_turn_sounds[0] == 0:
                        sound_list = [
                            explosion_sfx1, explosion_sfx2, explosion_sfx3, explosion_sfx4
                        ]
                        pygame.mixer.Sound.play(sound_list[random.randint(0, 3)])
                        pre_turn_sounds[0] = 1
                    if rounded_anim_ticks in range(31, 78):
                        if rounded_anim_ticks in range(31, 33):
                            explosion_img = explosion_frame_1
                        elif rounded_anim_ticks in range(33, 35):
                            explosion_img = explosion_frame_2
                        elif rounded_anim_ticks in range(35, 37):
                            explosion_img = explosion_frame_3
                        elif rounded_anim_ticks in range(37, 41):
                            explosion_img = explosion_frame_4
                        elif rounded_anim_ticks in range(41, 45):
                            explosion_img = explosion_frame_5
                        elif rounded_anim_ticks in range(45, 49):
                            explosion_img = explosion_frame_6
                        elif rounded_anim_ticks in range(53, 57):
                            explosion_img = explosion_frame_7
                        elif rounded_anim_ticks in range(57, 61):
                            explosion_img = explosion_frame_8
                        elif rounded_anim_ticks in range(61, 65):
                            explosion_img = explosion_frame_9
                        elif rounded_anim_ticks in range(65, 69):
                            explosion_img = explosion_frame_10
                        elif rounded_anim_ticks in range(69, 73):
                            explosion_img = explosion_frame_11
                        elif rounded_anim_ticks in range(73, 77):
                            explosion_img = explosion_frame_12
                        rightOverlay.blit(pygame.transform.scale_by(explosion_img, (1, 1)), (126+i*xdil-j*xdil+2, 37+i*ydil+j*ydil))
                else:
                    if rounded_anim_ticks >= 31 and pre_turn_sounds[0] == 0:
                        sound_list = [
                            splash_sfx1, splash_sfx2, splash_sfx3, splash_sfx4, splash_sfx5
                        ]
                        pygame.mixer.Sound.play(sound_list[random.randint(0, 4)])
                        pre_turn_sounds[0] = 1
                    if rounded_anim_ticks in range(31, 68):
                        if rounded_anim_ticks in range(31, 34):
                            splash_img = splash_frame_1
                        elif rounded_anim_ticks in range(34, 37):
                            splash_img = splash_frame_2
                        elif rounded_anim_ticks in range(37, 40):
                            splash_img = splash_frame_3
                        elif rounded_anim_ticks in range(40, 43):
                            splash_img = splash_frame_4
                        elif rounded_anim_ticks in range(43, 46):
                            splash_img = splash_frame_5
                        elif rounded_anim_ticks in range(46, 49):
                            splash_img = splash_frame_6
                        elif rounded_anim_ticks in range(49, 52):
                            splash_img = splash_frame_7
                        elif rounded_anim_ticks in range(52, 55):
                            splash_img = splash_frame_8
                        elif rounded_anim_ticks in range(55, 58):
                            splash_img = splash_frame_9
                        elif rounded_anim_ticks in range(58, 61):
                            splash_img = splash_frame_10
                        elif rounded_anim_ticks in range(61, 64):
                            splash_img = splash_frame_11
                        elif rounded_anim_ticks in range(64, 67):
                            splash_img = splash_frame_12
                        rightOverlay.blit(pygame.transform.scale_by(splash_img, (0.75, 0.75)), (134+i*xdil-j*xdil+2, 37+i*ydil+j*ydil))

        elif delay < rounded_anim_ticks <= delay + t:
            if Prev_action2 != [] and nuke_anim2 == True:
                Prev_action2.pop(0)
            if Prev_action2 != []:
                x = int(Prev_action2[0] % 10)
                y = int((Prev_action2[0]-x)/10)
                target_cell = pygame.Vector2(x, y)
                nuke_anim2 = True
                pre_turn_sounds = [0]
                anim_ticks = 0
                rounded_anim_ticks = 0
            else:
                if P2Boats_sunk[0] == 1 and P2Boats_sunk_visible[0] == 0:
                    P2Boats_sunk_visible[0] = 1
                elif P2Boats_sunk[1] == 1 and P2Boats_sunk_visible[1] == 0:
                    P2Boats_sunk_visible[1] = 1
                elif P2Boats_sunk[2] == 1 and P2Boats_sunk_visible[2] == 0:
                    P2Boats_sunk_visible[2] = 1
                elif P2Boats_sunk[3] == 1 and P2Boats_sunk_visible[3] == 0:
                    P2Boats_sunk_visible[3] = 1
                elif P2Boats_sunk[4] == 1 and P2Boats_sunk_visible[4] == 0:
                    P2Boats_sunk_visible[4] = 1
                if selectedPlayerMode == False and door_anim == False and P2Boats_sunk_visible == [1, 1, 1, 1, 1]:
                    door_anim = True
                    door_sounds = [0]
                    door_ticks = 0
                hud.blit(turn_banner_You, (0, 0))
                nuke_anim2 = False
                left_size = screen.get_width()/2 + scale*(1 - (0.5*t - (rounded_anim_ticks - delay))*diff)
                right_size = screen.get_width()/2 + scale*(1 + (0.5*t - (rounded_anim_ticks - delay))*diff)
                left_pos = pygame.Vector2(55, 50-(left_size*0.13))
                right_pos = pygame.Vector2(1225-right_size, 670-(right_size*0.69))
                anim_ticks += 1*dbltime * 60 * dt
                rounded_anim_ticks = round(anim_ticks)
        else:
            if nuke_anim == False and destroyer_sink_anim == False and submarine_sink_anim == False\
                and cruiser_sink_anim == False and battleship_sink_anim == False and carrier_sink_anim == False:
                x = selected_cell.x
                y = selected_cell.y
                if P1Boats[int(selected_cell.y)][int(selected_cell.x)] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    leftOverlay.blit(cursorX, (144+x*xdil-y*xdil, -13+x*ydil+y*ydil))
                else:
                    leftOverlay.blit(cursorC, (144+x*xdil-y*xdil, -13+x*ydil+y*ydil))
                if door_anim == False and (P1Boats_sunk == [1, 1, 1, 1, 1] or (time_enabled == True and P2Time <= 0)):
                    door_anim = True
                    door_sounds = [0]
                    door_ticks = 0

            if (keys[pygame.K_SPACE] or keys[pygame.K_e]) and nuke_anim == False and destroyer_sink_anim == False and submarine_sink_anim == False\
                and cruiser_sink_anim == False and battleship_sink_anim == False and carrier_sink_anim == False:
                if P1Boats[int(selected_cell.y)][int(selected_cell.x)] in [5, 15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                    pass
                else:
                    nuke_anim = True
                    nuke_ticks = 0
                    rounded_nuke_ticks = 0
                    sink_anim_ticks = 0
                    nuke_sounds = [0]
                    Prev_action.append(selected_cell.y*10 + selected_cell.x)

            if nuke_anim == True:
                x = int(selected_cell.x)
                y = int(selected_cell.y)
                target_cell = pygame.Vector2(x, y)
                if rounded_nuke_ticks <= 30:
                    leftOverlay.blit(pygame.transform.scale_by(nuke_img, (0.4, 0.4)), (144+x*xdil-y*xdil+2, (-13+x*ydil+y*ydil) - 5*(30-rounded_nuke_ticks)))
                if P1Boats[y][x] in [10, 11, 20, 21, 22, 30, 31, 32, 40, 41, 42, 43, 50, 51, 52, 53, 54]:
                    if rounded_nuke_ticks >= 31 and nuke_sounds[0] == 0:
                        sound_list = [
                            explosion_sfx1, explosion_sfx2, explosion_sfx3, explosion_sfx4
                        ]
                        pygame.mixer.Sound.play(sound_list[random.randint(0, 3)])
                        nuke_sounds[0] = 1
                    if rounded_nuke_ticks in range(31, 78):
                        if rounded_nuke_ticks in range(31, 33):
                            explosion_img = explosion_frame_1
                        elif rounded_nuke_ticks in range(33, 35):
                            explosion_img = explosion_frame_2
                        elif rounded_nuke_ticks in range(35, 37):
                            explosion_img = explosion_frame_3
                        elif rounded_nuke_ticks in range(37, 41):
                            explosion_img = explosion_frame_4
                        elif rounded_nuke_ticks in range(41, 45):
                            explosion_img = explosion_frame_5
                        elif rounded_nuke_ticks in range(45, 49):
                            explosion_img = explosion_frame_6
                        elif rounded_nuke_ticks in range(53, 57):
                            explosion_img = explosion_frame_7
                        elif rounded_nuke_ticks in range(57, 61):
                            explosion_img = explosion_frame_8
                        elif rounded_nuke_ticks in range(61, 65):
                            explosion_img = explosion_frame_9
                        elif rounded_nuke_ticks in range(65, 69):
                            explosion_img = explosion_frame_10
                        elif rounded_nuke_ticks in range(69, 73):
                            explosion_img = explosion_frame_11
                        elif rounded_nuke_ticks in range(73, 77):
                            explosion_img = explosion_frame_12
                        leftOverlay.blit(pygame.transform.scale_by(explosion_img, (1, 1)), (126+x*xdil-y*xdil+2, -10+x*ydil+y*ydil))
                else:
                    if rounded_nuke_ticks >= 31 and nuke_sounds[0] == 0:
                        sound_list = [
                            splash_sfx1, splash_sfx2, splash_sfx3, splash_sfx4, splash_sfx5
                        ]
                        pygame.mixer.Sound.play(sound_list[random.randint(0, 4)])
                        nuke_sounds[0] = 1
                    if rounded_nuke_ticks in range(31, 68):
                        if rounded_nuke_ticks in range(31, 34):
                            splash_img = splash_frame_1
                        elif rounded_nuke_ticks in range(34, 37):
                            splash_img = splash_frame_2
                        elif rounded_nuke_ticks in range(37, 40):
                            splash_img = splash_frame_3
                        elif rounded_nuke_ticks in range(40, 43):
                            splash_img = splash_frame_4
                        elif rounded_nuke_ticks in range(43, 46):
                            splash_img = splash_frame_5
                        elif rounded_nuke_ticks in range(46, 49):
                            splash_img = splash_frame_6
                        elif rounded_nuke_ticks in range(49, 52):
                            splash_img = splash_frame_7
                        elif rounded_nuke_ticks in range(52, 55):
                            splash_img = splash_frame_8
                        if rounded_nuke_ticks in range(55, 58):
                            splash_img = splash_frame_9
                        elif rounded_nuke_ticks in range(58, 61):
                            splash_img = splash_frame_10
                        elif rounded_nuke_ticks in range(61, 64):
                            splash_img = splash_frame_11
                        elif rounded_nuke_ticks in range(64, 67):
                            splash_img = splash_frame_12
                        leftOverlay.blit(pygame.transform.scale_by(splash_img, (0.75, 0.75)), (134+x*xdil-y*xdil+2, -12+x*ydil+y*ydil))

                nuke_ticks += 1*dbltime * 60 * dt
                rounded_nuke_ticks = round(nuke_ticks)

                if rounded_nuke_ticks > 120:
                    P1Boats[y][x] += 5
                    nuke_anim = False
                    if any(15 in sl for sl in P1Boats) and any(16 in sl for sl in P1Boats) and P1Boats_sunk[0] == 0:
                        destroyer_sink_anim = True
                        P1Boats_sunk[0] = 1
                    elif any(25 in sl for sl in P1Boats) and any(26 in sl for sl in P1Boats) and any(27 in sl for sl in P1Boats) and P1Boats_sunk[1] == 0:
                        submarine_sink_anim = True
                        P1Boats_sunk[1] = 1
                    elif any(35 in sl for sl in P1Boats) and any(36 in sl for sl in P1Boats) and any(37 in sl for sl in P1Boats) and P1Boats_sunk[2] == 0:
                        cruiser_sink_anim = True
                        P1Boats_sunk[2] = 1
                    elif any(45 in sl for sl in P1Boats) and any(46 in sl for sl in P1Boats) and any(47 in sl for sl in P1Boats) and any(48 in sl for sl in P1Boats) and P1Boats_sunk[3] == 0:
                        battleship_sink_anim = True
                        P1Boats_sunk[3] = 1
                    elif any(55 in sl for sl in P1Boats) and any(56 in sl for sl in P1Boats) and any(57 in sl for sl in P1Boats) and any(58 in sl for sl in P1Boats) and any(59 in sl for sl in P1Boats) and P1Boats_sunk[4] == 0:
                        carrier_sink_anim = True
                        P1Boats_sunk[4] = 1
                    if P1Boats[y][x] in [15, 16, 25, 26, 27, 35, 36, 37, 45, 46, 47, 48, 55, 56, 57, 58, 59]:
                        pass
                    else:
                        Prev_action2 = []
                        if time_enabled == True and P1Time <= 0:
                                switch("page router")
                        else:
                            door_anim = True
                            door_sounds = [0]

            if destroyer_sink_anim == True:
                sink_anim_ticks += 1*dbltime * 60 * dt
                
                if sink_anim_ticks == 1*dbltime * 60 * dt:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                sink_anim_ticks = round(sink_anim_ticks)

                if sink_anim_ticks > 120:
                    destroyer_sink_anim = False
            
            if submarine_sink_anim == True:
                sink_anim_ticks += 1*dbltime * 60 * dt
                
                if sink_anim_ticks == 1*dbltime * 60 * dt:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                sink_anim_ticks = round(sink_anim_ticks)

                if sink_anim_ticks > 120:
                    submarine_sink_anim = False

            if cruiser_sink_anim == True:
                sink_anim_ticks += 1*dbltime * 60 * dt
                
                if sink_anim_ticks == 1*dbltime * 60 * dt:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)
                
                sink_anim_ticks = round(sink_anim_ticks)

                if sink_anim_ticks > 120:
                    cruiser_sink_anim = False
            
            if battleship_sink_anim == True:
                sink_anim_ticks += 1*dbltime * 60 * dt
                
                if sink_anim_ticks == 1*dbltime * 60 * dt:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)
                
                sink_anim_ticks = round(sink_anim_ticks)

                if sink_anim_ticks > 120:
                    battleship_sink_anim = False
            
            if carrier_sink_anim == True:
                sink_anim_ticks += 1*dbltime * 60 * dt
                
                if sink_anim_ticks == 1*dbltime * 60 * dt:
                    offset = shake()
                    pygame.mixer.Sound.play(sink_sfx1)

                sink_anim_ticks = round(sink_anim_ticks)

                if sink_anim_ticks > 120:
                    carrier_sink_anim = False
                    
        hud.blit(hud_P2P1_img, (0, 0))

        if time_enabled == True:
            hud.blit(hud_time_img, (0, 0))

            if door_anim == False and nuke_anim == False and nuke_anim2 == False and rounded_anim_ticks > delay + t:
                P2Time -= dt  # Subtract time since last frame

                # Calculate minutes and seconds
            minutes = max(P2Time // 60, 0)  # Ensure minutes are not negative
            seconds = max(P2Time % 60, 0) # Ensure seconds are not negative
            
            timer_text = font3.render(f"{int(minutes):02d}:{int(seconds):02d}", True, (0, 0, 0))
            hud.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 3))
        
        control_text = [
            "-Move Cursor",
            "-Move Quicker",
            "",
            "-Fire"
        ]

        k = 0
        for icon in [controls_wasd_img, controls_shift_img, controls_space_img, controls_e_img]:
            if k == 0:
                hud.blit(pygame.transform.scale_by(icon, (1.2, 1.2)), (500, 655))
            elif k == 3:
                hud.blit(pygame.transform.scale_by(icon, (1.5, 1.5)), (520+120*2+45, 668))
            else:
                hud.blit(pygame.transform.scale_by(icon, (1.5, 1.5)), (520+120*k, 668))
            if k == 3:
                draw_text(f"{control_text[k]}", font5, (0, 0, 0), 530+130*2, 690)
            else:
                draw_text(f"{control_text[k]}", font5, (0, 0, 0), 530+130*k, 690)
            k += 1

        if door_anim == True:
            
            f = 2
            delay = 10
            if (door_ticks-delay) // f == f*0:
                switch_door = widgets.Image(640, 360, blast_door_8, 1)
            elif (door_ticks-delay) // f == f*1:
                switch_door = widgets.Image(640, 360, blast_door_7, 1)
            elif (door_ticks-delay) // f == f*2:
                switch_door = widgets.Image(640, 360, blast_door_6, 1)
            elif (door_ticks-delay) // f == f*3:
                switch_door = widgets.Image(640, 360, blast_door_5, 1)
            elif (door_ticks-delay) // f == f*4:
                switch_door = widgets.Image(640, 360, blast_door_4, 1)
            elif (door_ticks-delay)// f == f*5:
                switch_door = widgets.Image(640, 360, blast_door_3, 1)
            elif (door_ticks-delay) // f == f*6:
                switch_door = widgets.Image(640, 360, blast_door_2, 1)
            elif (door_ticks-delay) // f == f*7:
                switch_door = widgets.Image(640, 360, blast_door_1, 1)
            
            if door_ticks > delay:
                switch_door.draw(hud)

            if door_ticks >= 1 and door_sounds[0] == 0:
                pygame.mixer.Sound.play(door_close_sfx)
                door_sounds[0] = 1

            if door_ticks > 30:
                door_anim = False
                switch("page router")

            door_ticks += 1 * 60 * dt
    

    elif game_screen == "win":
        screen.blit(pygame.transform.scale(ocean_screen, (1280, 720)), (0, 0))
        screen.blit(split_Board_img, (0, 0))
        if winner == "AI (Easy)":
            AI1Icon.draw(hud)
        elif winner == "AI (Hard)":
            AI2Icon.draw(hud)
        elif winner == "Player 1":
            P1Icon.draw(hud)
        else:
            P2Icon.draw(hud)
        draw_text(f"Winner: {winner}", font1, (0, 0, 0), 320-font1.size(f"Winner: {winner}")[0]/2, 50)
        draw_text(f"Against {loser}", font3, (0, 0, 0), 320-font3.size(f"Against {loser}")[0]/2, 115)
        i = 0
        idx = 0
        quote_wrap = ""
        while True:
            while True:
                if idx == len(quote.split()):
                    break
                if font3.size(quote_wrap + " " + quote.split()[idx])[0] > 550:
                    break
                quote_wrap = quote_wrap + " " + quote.split()[idx]
                idx += 1

            draw_text(f"{quote_wrap}", font3, (0, 0, 0), 320-font3.size(f"{quote_wrap}")[0]/2, 550 + 35*i)
            quote_wrap = ""
            i += 1
            if idx == len(quote.split()):
                break

        draw_text("Battle Report", font1, (0, 0, 0), 960-font1.size("Battle Report")[0]/2, 50)
        draw_text(f"Shots Taken: {shotCount}", font3, (0, 0, 0), 960-font3.size(f"Shots Taken: {shotCount}")[0]/2, 125)
        draw_text(f"Accuracy: {accuracy}%", font3, (0, 0, 0), 960-font3.size(f"Accuracy: {accuracy}%")[0]/2, 175)
        draw_text(f"Turns Taken: {turnCount}", font3, (0, 0, 0), 960-font3.size(f"Turns Taken: {turnCount}")[0]/2, 225)
        draw_text(f"Average Shots Per Turn: {spt}", font3, (0, 0, 0), 960-font3.size(f"Average Shots Per Turn: {spt}")[0]/2, 275)

        if backButton3.draw(hud):
            pygame.mixer.Sound.play(blip)
            switch("main")

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

            door_ticks += 1 * 60 * dt
    
    elif game_screen == "Grid View":
        pass
        

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
    
    dt = clock.tick(FPS) / 1000
    screen.blit(pygame.transform.scale(placementSurface, (screen.get_width()/1.5, screen.get_width()/1.5)), (440, 50))
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