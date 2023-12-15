import sys
with open(sys.argv[1]) as f:
    textgrid = f.read().rstrip().split('\n')

w = len(textgrid[0])
h = len(textgrid)

squares = set()
rounds = set()
for y, row in enumerate(textgrid):
    for x, char in enumerate(row):
        if char == '#':
            squares.add((x, y))
        if char == 'O':
            rounds.add((x, y))

def pgrid(squares, rounds):
    for y in range(h):
        for x in range(w):
            c = '.'
            if (x, y) in squares:
                c = '#'
            elif (x, y) in rounds:
                c = 'O'
            print(c, end='')
        print()


def roll_north(rounds, squares):
    for y in range(h):
        for x in range(w):
            if (x, y) in rounds:
                rounds.remove((x, y))
                yy = y
                while True:
                    yy -= 1
                    if yy < 0 or (x, yy) in squares|rounds:
                        yy += 1
                        break
                rounds.add((x, yy))

def roll_south(rounds, squares):
    for y in reversed(range(h)):
        for x in range(w):
            if (x, y) in rounds:
                rounds.remove((x, y))
                yy = y
                while True:
                    yy += 1
                    if yy >= h or (x, yy) in squares|rounds:
                        yy -= 1
                        break
                rounds.add((x, yy))

def roll_west(rounds, squares):
    for x in range(w):
        for y in range(h):
            if (x, y) in rounds:
                rounds.remove((x, y))
                xx = x
                while True:
                    xx -= 1
                    if xx < 0 or (xx, y) in squares|rounds:
                        xx += 1
                        break
                rounds.add((xx, y))

def roll_east(rounds, squares):
    for x in reversed(range(w)):
        for y in range(h):
            if (x, y) in rounds:
                rounds.remove((x, y))
                xx = x
                while True:
                    xx += 1
                    if xx >= w or (xx, y) in squares|rounds:
                        xx -= 1
                        break
                rounds.add((xx, y))


def load(rounds):
    return sum([(h - y) for (x, y) in rounds])

cache = {}
cache_iter = {}

inp = frozenset(rounds)
for i in range(1000000000):
    print(len(cache))
    if inp in cache:
        loop_start = cache_iter[inp]
        loop_end = i
        loop_length = loop_end - loop_start
        print("loop", loop_start, loop_end)
        loops = (1000000000 - loop_start) // loop_length
        rem = (1000000000 - loop_start) % loop_length
        print(loops, rem)
        for i in range(rem):
            inp = cache[inp]
        rounds = set(inp)
        break

    print('rolling north')
    roll_north(rounds, squares)
    print('rolling west')
    roll_west(rounds, squares)
    print('rolling south')
    roll_south(rounds, squares)
    print('rolling east')
    roll_east(rounds, squares)

    #print(load(rounds))
    #pgrid(squares, rounds)

    o = frozenset(rounds)
    cache[inp] = o
    cache_iter[inp] = i
    inp = o

pgrid(squares, rounds)
print()
print(load(rounds))
