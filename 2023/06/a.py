with open("input.txt") as f:
    times = [int(i) for i in next(f).split()[1:]]
    dists = [int(i) for i in next(f).split()[1:]]
print(times, dists)

total = 1
for time, best_d in zip(times, dists):
    #print(f'race with time {time} and best {best_d}')
    ways_to_win = 0
    for held in range(1, time):
        speed = held
        travel = held * (time - held)
        #print(f'holding {held} travels {travel}')
        if travel > best_d:
            ways_to_win += 1
    total *= ways_to_win

print(total)
