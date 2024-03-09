import pygame
import copy
import random
game_screen = "page router"
inGame = False
selectedPlayerMode = False
playersReady = 0
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
P1Rot = []
P1Boats_sunk = []
P2Boats = []
P2Rot = []
P2Boats_sunk = []
BoatRotation = 0
turn = 0
time_enabled = False
P1Time = 0
P2Time = 0
difficulty = "Easy"


# function to switch game screen, also prints for debug
def switch(screen):
    global game_screen
    game_screen = screen
    print(screen)

# This module redirects users to the next screen based on certain criteria.
# All decision-making concerning which screen to use is done here in order to see where each screen goes with certain conditions.
# Does not involve first few screens as they move in a more linear fashion, with the main menu as a pseudo-hub

if game_screen == "page router":
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
                pygame.mixer.music.load("sounds/Music/Enemy Ship Approaching.ogg")
            else:
                pygame.mixer.music.load("sounds/Music/restless sea.wav")
            pygame.mixer.music.play()
            switch("win")