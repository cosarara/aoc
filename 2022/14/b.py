def make_cave(inp):
    cave = {}
    for line in inp.strip().split('\n'):
        points = [[int(c) for c in p.split(',')]
                    for p in line.split(' -> ')]
        for i in range(1, len(points)):
            x0, y0 = points[i-1]
            x1, y1 = points[i]
            for x in range(min(x0, x1), max(x0, x1)+1):
                for y in range(min(y0, y1), max(y0, y1)+1):
                    cave[(x, y)] = '#'
    return cave

def drip(cave, floor):
    x, y = (500, 0)
    while True:
        if y+1 == floor: # endless floor
            break
        if (x, y+1) not in cave:
            y += 1
        elif (x-1, y+1) not in cave:
            y += 1
            x -= 1
        elif (x+1, y+1) not in cave:
            y += 1
            x += 1
        else:
            break
    if (x, y) == (500, 0):
        return False
    cave[(x, y)] = 'o'
    return True


def draw_cave(cave, floor):
    minx = min(x for x, y in cave)
    maxx = max(x for x, y in cave)
    miny = min(y for x, y in cave)
    maxy = max(y for x, y in cave)+2
    for y in range(miny, maxy+1):
        print(''.join((cave[(x, y)] if (x, y) in cave else
                       '#' if y == floor else '.')
              for x in range(minx, maxx+1)))

with open('input') as f:
    import sys
    inp = sys.stdin.read()

c = make_cave(inp)
floor = max(y for x, y in c)+2
i = 0
while True:
#for i in range(100):
    i += 1
    if not drip(c, floor):
        break
    #draw_cave(c)
draw_cave(c, floor)
print(i)
