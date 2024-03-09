import pygame
import sys
import os

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

pygame.init()

# set surfaces
org_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),0,32) #parent screen
screen = org_screen.copy() #buffer screen, used to screen-shake. All children are blit to this surface, and this surface is blit to org_screen
placementSurface = pygame.Surface((400, 400)).convert_alpha() #renders grid for boat placement

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

# import sea assets
sea_anim_cd = 0
cur_sea = 0
d_sea_tile = pygame.image.load(resource_path("images\isometric tiles\sea unit.png")).convert_alpha()
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

TestGrid = [
    [10, 11, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [20, 21, 22, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [30, 31, 32, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [40, 41, 42, 43, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [50, 51, 52, 53, 54, 00, 00, 00, 00, 00, 99, 99, 99, 99],
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

TestGrid2 = [
    [15, 16, 00, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [25, 26, 27, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [35, 36, 37, 00, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [45, 46, 47, 48, 00, 00, 00, 00, 00, 00, 99, 99, 99, 99],
    [55, 56, 57, 58, 59, 00, 00, 00, 00, 00, 99, 99, 99, 99],
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

# key: 00, 0: empty tile (sea tile)
#     5: empty tile hit (miss) (no hit sea tile)
#     10, 11: destroyer
#     15, 16: destroyer hit
#     20, 21, 22: submarine
#     25, 26, 27: submarine hit
#     30, 31, 32: cruiser
#     35, 36, 37: cruiser hit
#     40, 41, 42, 43: battleship
#     45, 46, 47, 48: battleship hit
#     50, 51, 52, 53, 54: carrier
#     55, 56, 57, 58, 59: carrier hit

InputGrid = TestGrid

BoatRotation = [0, 0, 0, 0, 0] # stores boat directions during placement, 0 to the right, 1 to the left

running = True
tick = 0
while running:
    org_screen.fill((0, 0, 0, 0))
    screen.fill((110, 110, 110))
    placementSurface.fill((0, 0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    xdil = 16
    ydil = 8
    # render grid labels
    for y, row in enumerate(InputGrid):
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
    for y, row in enumerate(InputGrid):
        for x, tile in enumerate(row):
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
                        }
            # grab tile sprite using tile ID
            tile_sprite = funcs.get(tile, "blank")

            # switch animation frames based on tick count
            if tile == 15:
                if tick in range(0, 30):
                    tile_sprite = destroyer2_sink1
                elif tick in range(30, 60):
                    tile_sprite = destroyer2_sink2
                elif tick in range(60, 90):
                    tile_sprite = destroyer2_sink3
                elif tick in range(90, 120):
                    tile_sprite = destroyer2_sink4
                elif tick in range(90, 210):
                    tile_sprite = destroyer2_sink5
                elif tick in range(210, 330):
                    tile_sprite = destroyer2_sink1
            if tile == 16:
                if tick in range(0, 30):
                    tile_sprite = destroyer1_sink1
                elif tick in range(30, 60):
                    tile_sprite = destroyer1_sink2
                elif tick in range(60, 90):
                    tile_sprite = destroyer1_sink3
                elif tick in range(90, 120):
                    tile_sprite = destroyer1_sink4
                elif tick in range(90, 210):
                    tile_sprite = destroyer1_sink5
                elif tick in range(210, 330):
                    tile_sprite = destroyer1_sink1
            if tile == 25:
                if tick in range(0, 30):
                    tile_sprite = submarine3_sink1
                elif tick in range(30, 60):
                    tile_sprite = submarine3_sink2
                elif tick in range(60, 90):
                    tile_sprite = submarine3_sink3
                elif tick in range(90, 120):
                    tile_sprite = submarine3_sink4
                elif tick in range(90, 210):
                    tile_sprite = submarine3_sink5
                elif tick in range(210, 330):
                    tile_sprite = submarine3_sink1
            if tile == 26:
                if tick in range(0, 30):
                    tile_sprite = submarine2_sink1
                elif tick in range(30, 60):
                    tile_sprite = submarine2_sink2
                elif tick in range(60, 90):
                    tile_sprite = submarine2_sink3
                elif tick in range(90, 120):
                    tile_sprite = submarine2_sink4
                elif tick in range(90, 210):
                    tile_sprite = submarine2_sink5
                elif tick in range(210, 330):
                    tile_sprite = submarine2_sink1
            if tile == 27:
                if tick in range(0, 30):
                    tile_sprite = submarine1_sink1
                elif tick in range(30, 60):
                    tile_sprite = submarine1_sink2
                elif tick in range(60, 90):
                    tile_sprite = submarine1_sink3
                elif tick in range(90, 120):
                    tile_sprite = submarine1_sink4
                elif tick in range(90, 210):
                    tile_sprite = submarine1_sink5
                elif tick in range(210, 330):
                    tile_sprite = submarine1_sink1
            if tile == 35:
                if tick in range(0, 30):
                    tile_sprite = cruiser3_sink1
                elif tick in range(30, 60):
                    tile_sprite = cruiser3_sink2
                elif tick in range(60, 90):
                    tile_sprite = cruiser3_sink3
                elif tick in range(90, 120):
                    tile_sprite = cruiser3_sink4
                elif tick in range(90, 210):
                    tile_sprite = cruiser3_sink5
                elif tick in range(210, 330):
                    tile_sprite = cruiser3_sink1
            if tile == 36:
                if tick in range(0, 30):
                    tile_sprite = cruiser2_sink1
                elif tick in range(30, 60):
                    tile_sprite = cruiser2_sink2
                elif tick in range(60, 90):
                    tile_sprite = cruiser2_sink3
                elif tick in range(90, 120):
                    tile_sprite = cruiser2_sink4
                elif tick in range(90, 210):
                    tile_sprite = cruiser2_sink5
                elif tick in range(210, 330):
                    tile_sprite = cruiser2_sink1
            if tile == 37:
                if tick in range(0, 30):
                    tile_sprite = cruiser1_sink1
                elif tick in range(30, 60):
                    tile_sprite = cruiser1_sink2
                elif tick in range(60, 90):
                    tile_sprite = cruiser1_sink3
                elif tick in range(90, 120):
                    tile_sprite = cruiser1_sink4
                elif tick in range(90, 210):
                    tile_sprite = cruiser1_sink5
                elif tick in range(210, 330):
                    tile_sprite = cruiser1_sink1
            if tile == 45:
                if tick in range(0, 30):
                    tile_sprite = battleship4_sink1
                elif tick in range(30, 60):
                    tile_sprite = battleship4_sink2
                elif tick in range(60, 90):
                    tile_sprite = battleship4_sink3
                elif tick in range(90, 120):
                    tile_sprite = battleship4_sink4
                elif tick in range(90, 210):
                    tile_sprite = battleship4_sink5
                elif tick in range(210, 330):
                    tile_sprite = battleship4_sink1
            if tile == 46:
                if tick in range(0, 30):
                    tile_sprite = battleship3_sink1
                elif tick in range(30, 60):
                    tile_sprite = battleship3_sink2
                elif tick in range(60, 90):
                    tile_sprite = battleship3_sink3
                elif tick in range(90, 120):
                    tile_sprite = battleship3_sink4
                elif tick in range(90, 210):
                    tile_sprite = battleship3_sink5
                elif tick in range(210, 330):
                    tile_sprite = battleship3_sink1
            if tile == 47:
                if tick in range(0, 30):
                    tile_sprite = battleship2_sink1
                elif tick in range(30, 60):
                    tile_sprite = battleship2_sink2
                elif tick in range(60, 90):
                    tile_sprite = battleship2_sink3
                elif tick in range(90, 120):
                    tile_sprite = battleship2_sink4
                elif tick in range(90, 210):
                    tile_sprite = battleship2_sink5
                elif tick in range(210, 330):
                    tile_sprite = battleship2_sink1
            if tile == 48:
                if tick in range(0, 30):
                    tile_sprite = battleship1_sink1
                elif tick in range(30, 60):
                    tile_sprite = battleship1_sink2
                elif tick in range(60, 90):
                    tile_sprite = battleship1_sink3
                elif tick in range(90, 120):
                    tile_sprite = battleship1_sink4
                elif tick in range(90, 210):
                    tile_sprite = battleship1_sink5
                elif tick in range(210, 330):
                    tile_sprite = battleship1_sink1
            if tile == 55:
                if tick in range(0, 30):
                    tile_sprite = carrier5_sink1
                elif tick in range(30, 60):
                    tile_sprite = carrier5_sink2
                elif tick in range(60, 90):
                    tile_sprite = carrier5_sink3
                elif tick in range(90, 120):
                    tile_sprite = carrier5_sink4
                elif tick in range(90, 210):
                    tile_sprite = carrier5_sink5
                elif tick in range(210, 330):
                    tile_sprite = carrier5_sink1
            if tile == 56:
                if tick in range(0, 30):
                    tile_sprite = carrier4_sink1
                elif tick in range(30, 60):
                    tile_sprite = carrier4_sink2
                elif tick in range(60, 90):
                    tile_sprite = carrier4_sink3
                elif tick in range(90, 120):
                    tile_sprite = carrier4_sink4
                elif tick in range(90, 210):
                    tile_sprite = carrier4_sink5
                elif tick in range(210, 330):
                    tile_sprite = carrier4_sink1
            if tile == 57:
                if tick in range(0, 30):
                    tile_sprite = carrier3_sink1
                elif tick in range(30, 60):
                    tile_sprite = carrier3_sink2
                elif tick in range(60, 90):
                    tile_sprite = carrier3_sink3
                elif tick in range(90, 120):
                    tile_sprite = carrier3_sink4
                elif tick in range(90, 210):
                    tile_sprite = carrier3_sink5
                elif tick in range(210, 330):
                    tile_sprite = carrier3_sink1
            if tile == 58:
                if tick in range(0, 30):
                    tile_sprite = carrier2_sink1
                elif tick in range(30, 60):
                    tile_sprite = carrier2_sink2
                elif tick in range(60, 90):
                    tile_sprite = carrier2_sink3
                elif tick in range(90, 120):
                    tile_sprite = carrier2_sink4
                elif tick in range(90, 210):
                    tile_sprite = carrier2_sink5
                elif tick in range(210, 330):
                    tile_sprite = carrier2_sink1
            if tile == 59:
                if tick in range(0, 30):
                    tile_sprite = carrier1_sink1
                elif tick in range(30, 60):
                    tile_sprite = carrier1_sink2
                elif tick in range(60, 90):
                    tile_sprite = carrier1_sink3
                elif tick in range(90, 120):
                    tile_sprite = carrier1_sink4
                elif tick in range(90, 210):
                    tile_sprite = carrier1_sink5
                elif tick in range(210, 330):
                    tile_sprite = carrier1_sink1

                    
            # boat type detection
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
            
            # check boat orientation
            if boat_type != 9:
                if BoatRotation[boat_type] == 0:
                    rotate_cell = False
                elif BoatRotation[boat_type] == 1:
                    rotate_cell = True
            
            # render playing board
            if tile_sprite == "blank":
                pass
            elif rotate_cell == False:
                placementSurface.blit(tile_sprite, (183+x*xdil-y*xdil, 0+x*ydil+y*ydil))
            elif rotate_cell == True:
                placementSurface.blit(pygame.transform.flip(tile_sprite, True, False), (183+x*xdil-y*xdil, 0+x*ydil+y*ydil))
            elif tile_sprite == d_sea_tile:
                placementSurface.blit(tile_sprite, (183+x*xdil-y*xdil, 0+x*ydil+y*ydil))
            else:
                placementSurface.blit(pygame.transform.flip(tile_sprite, True, False), (183+x*xdil-y*xdil, 0+x*ydil+y*ydil))
    
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
        sea_anim_cd = 90
    
    sea_anim_cd -= 1

    tick += 1
    if tick >= 330:
        tick = 0
    
    screen.blit(pygame.transform.scale(placementSurface, (screen.get_width()/1.5, screen.get_width()/1.5)), (640-screen.get_width()/3, 360-screen.get_height()/3))
    org_screen.blit(screen, (0, 0))
    pygame.display.update()
