#head or tails
import random
choice = input("H/T: ")
funcs: dict = {"H": 0,
               "h": 0,
               "T": 1,
               "t": 1}
rnum = random.randint(0,1)
print(f"You chose: {funcs.get(choice)}")
print(f"Coin rolled: {rnum}")
if funcs.get(choice) == rnum:
    print("die")