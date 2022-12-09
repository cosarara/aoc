def up(coords):
    coords[1] += 1

def down(coords):
    coords[1] -= 1

def right(coords):
    coords[0] += 1

def left(coords):
    coords[0] -= 1

head = [0,0]
tail = [0,0]

# chess distance
def dist(head, tail):
    return max(abs(head[0]-tail[0]), abs(head[1]-tail[1]))

visited = set()

def move(direction):
    f = {'U': up,
         'D': down,
         'R': right,
         'L': left}[direction]
    f(head)
    if dist(head, tail) >= 2:
        f(tail)
        if direction in 'UD':
            tail[0] = head[0] # match x
        else:
            tail[1] = head[1] # match y
    visited.add(tuple(tail))

import sys
text = sys.stdin.read()

def draw():
    # print map
    h, w = (20, 20)
    for y in range(h, -1, -1):
        for x in range(w):
            if head == [x, y]:
                print('H', end='')
            elif tail == [x, y]:
                print('T', end='')
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

print(len(visited))
