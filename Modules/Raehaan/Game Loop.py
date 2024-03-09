import pygame
import sys
import os


# Game module, P2Game is identical to P1Game, but without any logic related to AI and one player mode
if game_screen == "P1Game":
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