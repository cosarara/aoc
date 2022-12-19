import itertools
shapes = iter(itertools.cycle([
    ['####'],

    ['.#.',
     '###',
     '.#.'],

    ['..#',
     '..#',
     '###'],

    ['#',
     '#',
     '#',
     '#'],

    ['##',
     '##']
]))

cave = set() # coords of solid rocks

with open("input") as f:
    text = f.read().strip()
# example
# text = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
jets = iter(
    itertools.cycle(text))

def shift(shape, x, y, jet):
    if jet == '>' and x+len(shape[0]) < 7:
        xx = x+1
    elif jet == '<' and x-1 >= 0:
        xx = x-1
    else:
        return x
    # check against rocks
    for sy, line in enumerate(reversed(shape)):
        for sx, char in enumerate(line):
            if char == '#':
                if (sx+xx, sy+y) in cave:
                    return x
    return xx

def drop_collided(shape, x, yy):
    if yy < 0:
        return True
    # check against rocks
    for sy, line in enumerate(reversed(shape)):
        for sx, char in enumerate(line):
            if char == '#':
                if (sx+x, sy+yy) in cave:
                    return True
    return False

def shape_coords(x, y, shape):
    coords = set()
    for sy, line in enumerate(reversed(shape)):
        for sx, char in enumerate(line):
            if char == '#':
                coords.add((sx+x, sy+y))
    return coords

def draw(shape, x, y):
    c = shape_coords(x, y, shape)
    for y in range(y+4, -1, -1):
        print('|', end='')
        for x in range(7):
            if (x, y) in cave:
                print('#', end='')
            elif (x, y) in c:
                print('@', end='')
            else:
                print('.', end='')
        print('|')
    print('+-------+')

highest = 0
for i in range(2022):
    shape = next(shapes)
    x = 2
    y = highest + 3
    #draw(shape, x, y)
    while True:
        jet = next(jets)
        x = shift(shape, x, y, jet)
        yy = y-1
        if drop_collided(shape, x, yy):
            break
        else:
            y = yy
    # solidify
    highest = max(highest, y+len(shape))
    cave |= shape_coords(x, y, shape)

print(highest)
