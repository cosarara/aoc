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

def drip(cave):
    x, y = (500, 0)
    maxy = max(y for x, y in cave)
    while True:
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
        if y > maxy:
            return False
    cave[(x, y)] = 'o'
    return True


def draw_cave(cave):
    minx = min(x for x, y in cave)
    maxx = max(x for x, y in cave)
    miny = min(y for x, y in cave)
    maxy = max(y for x, y in cave)
    for y in range(miny, maxy+1):
        print(''.join((cave[(x, y)] if (x, y) in cave else '.')
              for x in range(minx, maxx+1)))

with open('input') as f:
    import sys
    inp = sys.stdin.read()

c = make_cave(inp)
i = 0
while True:
    if not drip(c):
        break
    i += 1
draw_cave(c)
print(i)
