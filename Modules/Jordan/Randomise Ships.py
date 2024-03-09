import random

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
BoatRotation = [0, 0, 0, 0, 0]

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
                if rot == 0 and BlankGrid[y][x+i] != 00:
                    bad_cell = True
                if rot == 1 and BlankGrid[y+i][x] != 00:
                    bad_cell = True
        if bad_cell == False:
            for e in range(0, cur_boat_len):
                if rot == 0:
                    BlankGrid[y][x+e] = boat_count*10 + e
                    BoatRotation[boat_count - 1] = 0
                if rot == 1:
                    BlankGrid[y+e][x] = boat_count*10 + e
                    BoatRotation[boat_count - 1] = 1

for i in BlankGrid:
    print(i)