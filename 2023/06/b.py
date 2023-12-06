with open("input.txt") as f:
    time = int(''.join(next(f).split()[1:]))
    best_d = int(''.join(next(f).split()[1:]))
print(time, best_d)

#print(f'race with time {time} and best {best_d}')
ways_to_win = 0
for held in range(1, time):
    speed = held
    travel = held * (time - held)
    #print(f'holding {held} travels {travel}')
    if travel > best_d:
        ways_to_win += 1

print(ways_to_win)
