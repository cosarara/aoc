def up(coords):
    coords[1] += 1

def down(coords):
    coords[1] -= 1

def right(coords):
    coords[0] += 1

def left(coords):
    coords[0] -= 1

rope = [[0,0] for _ in range(10)]

# chess distance
def dist(head, tail):
    return max(abs(head[0]-tail[0]), abs(head[1]-tail[1]))

visited = set()

def close_gap(head, tail):
    # find the best reachable gap closer
    for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1),
                     (1, 1), (1, -1), (-1, 1), (-1, -1)):
        x, y = (head[0]+dx, head[1]+dy) # desirable spot
        if dist(tail, (x, y)) == 1: # reachable
            tail[0] = x
            tail[1] = y
            break

def move(direction):
    f = {'U': up,
         'D': down,
         'R': right,
         'L': left}[direction]
    f(rope[0])
    for i in range(9):
        head = rope[i]
        tail = rope[i+1]
        if dist(head, tail) >= 2:
            close_gap(head, tail)
    visited.add(tuple(rope[9]))

import sys
text = sys.stdin.read()

def draw():
    # print map
    h, w = (20, 20)
    for y in range(h, -1, -1):
        for x in range(w):
            if [x, y] in rope:
                print(rope.index([x, y]), end='')
            elif (x, y) in visited:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()

moves = [l.split() for l in text.strip().split('\n')]
for direction, count in moves:
    for i in range(int(count)):
        move(direction)
        draw()

print(len(visited))
