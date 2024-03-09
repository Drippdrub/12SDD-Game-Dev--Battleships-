import pygame
import sys
import os

# used for pyinstaller compatability
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
screen = pygame.display.set_mode((1280, 720))

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