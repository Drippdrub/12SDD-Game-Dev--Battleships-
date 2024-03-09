import pygame
import random

AI_hit_reg = []

P1Boats = [
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

P2Boats = [
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

# function to switch game screen, also prints for debug
def switch(screen):
    global game_screen
    game_screen = screen
    print(screen)

difficulty = "Hard"
Prev_action = [] #stores actions for animation for player 1
locked_on_ship = False
uncleared_cells = []
unfairness_multiplier = 0
P1Boats_sunk = [0, 0, 0, 0, 0]


# put inside loop
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
                # if checked both directions and no ship sunk, unlock and resolve cases (when ships are bunched up)
                if double_check == 2:
                    locked_on_ship = False
                    double_check = 0
                    lock = False