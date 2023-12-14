from math import sqrt, ceil, floor

distance = lambda held, time : held * (time - held)

def calc(time, best_d):
    start = ceil((-time + sqrt(time*time - 4*best_d)) / -2)
    if distance(start, time) == best_d:
        start += 1

    end = floor((-time - sqrt(time*time - 4*best_d)) / -2)
    if distance(end, time) == best_d:
        end -= 1

    print(start, distance(start, time), end, distance(end, time))
    ways = end - start + 1 # inclusive
    print(ways)
    return ways

#assert calc(7, 9) == 4
#assert calc(15, 40) == 8
#assert calc(30, 200) == 9


with open("input.txt") as f:
    time = int(''.join(next(f).split()[1:]))
    best_d = int(''.join(next(f).split()[1:]))
calc(time, best_d)
