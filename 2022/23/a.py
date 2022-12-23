import sys
from collections import defaultdict
def add(c, d):
    return (c[0]+d[0], c[1]+d[1])

N = (0, -1)
NE = (1, -1)
NW = (-1, -1)
S = (0, 1)
SE = (1, 1)
SW = (-1, 1)
W = (-1, 0)
E = (1, 0)

checks = [
    (N, NE, NW),
    (S, SE, SW),
    (W, NW, SW),
    (E, NE, SE)
]

all_regions = [N, NE, NW, S, SE, SW, W, E]

elves = []
for y, l in enumerate(sys.stdin.read().strip().split('\n')):
    for x, c in enumerate(l):
        if c == '#':
            elves.append((x, y))

def draw():
    minx = min(x for x,y in elves)
    maxx = max(x for x,y in elves)
    miny = min(y for x,y in elves)
    maxy = max(y for x,y in elves)

    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            print('#' if (x,y) in elves else '.', end='')
        print()

    w = maxx - minx+1
    h = maxy - miny+1
    print(w,h)
    print(w*h-len(elves))

turn = 0
while True:
    turn += 1
    print('TURN', turn)
    proposals = defaultdict(list)
    selves = set(elves)
    for n, elfpos in enumerate(elves):
        if not any(add(spot, elfpos) in selves
                   for spot in all_regions):
            continue # don't need to move
        for region in checks:
            if not any(add(spot, elfpos) in selves
                       for spot in region):
                proposals[add(elfpos, region[0])].append(n)
                break
    #print(proposals)
    if not proposals:
        print('we are done', turn)
        break
    for proposal, pelves in proposals.items():
        if len(pelves) == 1:
            # move the elf
            elves[pelves[0]] = proposal
    # cycle the checks thing
    c = checks.pop(0)
    checks.append(c)
    #print(checks)

    #draw()
