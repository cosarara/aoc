with open("input.txt") as f:
    lines = [l.strip('\n') for l in f]

def get_points(line):
    _, d = line.split(": ")
    wins, haves = d.split(" | ")
    nwins = len(set(wins.split()) & set(haves.split()))
    if nwins == 0:
        return 0
    elif nwins == 1:
        return 1
    return 2**(nwins-1)

print(sum(get_points(l) for l in lines))

