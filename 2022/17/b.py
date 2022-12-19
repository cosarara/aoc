shapes = (
    ('####',),

    ('.#.',
     '###',
     '.#.'),

    ('..#',
     '..#',
     '###'),

    ('#',
     '#',
     '#',
     '#'),

    ('##',
     '##')
)

cave = set() # coords of solid rocks

with open("input") as f:
    jets = f.read().strip()

# example
#jets = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

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
jeti = 0
states_seen = {}
heights = {}
target = 1_000_000_000_000
#target = 2022
for i in range(target):
    shape = shapes[i%5]
    x = 2
    y = highest + 3
    #draw(shape, x, y)
    while True:
        jet = jets[jeti]
        jeti += 1
        jeti %= len(jets)
        x = shift(shape, x, y, jet)
        #print('shift')
        #draw(shape, x, y)
        yy = y-1
        if drop_collided(shape, x, yy):
            break
        else:
            y = yy
        #print('drop')
        #draw(shape, x, y)
    # solidify
    highest = max(highest, y+len(shape))
    cave |= shape_coords(x, y, shape)

    heights[i] = highest

    # pattern
    if highest > 50:
        pattern = set()
        for y in range(highest-50, highest):
            for x in range(7):
                if (x, y) in cave:
                    pattern.add((x, y-highest))
        state = (i%5, jeti, frozenset(pattern))
        if state in states_seen:
            # 1 2 0 5 10 0 5 10
            #     ^      ^
            # i=5 loop found
            # i=2 loop start (i0)
            # loop length -> 3 (5 - 2)
            # loop height = h[i-1] - h[i0]
            i0 = states_seen[state]
            loop_length = i - i0
            preloop_h = heights[i0-1]
            loop_height = heights[i-1] - preloop_h
            loops_to_end = (target - i0) // loop_length
            extra =        (target - i0) % loop_length
            extra_h = heights[i0+extra-1] - preloop_h
            #if extra == 0:
            print("loop found!", i, i0)
            print("each loop takes", loop_length, "blocks")
            print("height before the first loop was", preloop_h)
            print("each loop is", loop_height, "units high")
            print("to reach block", target, "we will need",
                  loops_to_end, "loops")
            print("and then", extra, "blocks more")
            print("that will give us", extra_h, "units more")
            print("total height:", loop_height * loops_to_end +
                  extra_h
                  + preloop_h)
            break
        #else:
        #    states_seen[state] = i
        states_seen[state] = i


print(highest)
