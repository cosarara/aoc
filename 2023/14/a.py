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


def roll(rounds, squares):
    rounds = set(rounds)
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
    return rounds

def load(rounds):
    return sum([(h - y) for (x, y) in rounds])

pgrid(squares, rounds)
print()
rolled = roll(rounds, squares)
pgrid(squares, rolled)
print()
print(load(rolled))
