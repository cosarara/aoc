import sys

walls = set()
resp = {} # respawn after crashing
blizzards_0 = []
blizzard_pos_0 = set()
initial_map = sys.stdin.read().strip().split('\n')
print(initial_map)
h = len(initial_map)
w = len(initial_map[0])

end = (w-2, h-1)
print('w', w)
print('h', h)
print('end', end)

for y, line in enumerate(initial_map):
    for x, char in enumerate(line):
        if char in '><^v':
            blizzards_0.append(((x, y), char))
            blizzard_pos_0.add((x, y))
        elif char == '#':
            walls.add((x, y))
            if x == 0:
                resp[(x, y)] = (w-2, y)
            elif x == w-1:
                resp[(x, y)] = (1, y)
            elif y == 0:
                resp[(x, y)] = (x, h-2)
            elif y == h-1:
                resp[(x, y)] = (x, 1)
            else:
                raise Exception('ur a baka', x, y)
print('reading done')

deltas = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'v': (0, 1)
}

def a(p, q):
    return p[0]+q[0], p[1]+q[1]

def blizzard_next(blizzard):
    (x, y), d = blizzard
    n = a((x, y), deltas[d])
    try:
        return (resp[n], d)
    except KeyError:
        return (n, d)

blizzards = {0: blizzards_0}
blizzard_pos = {0: blizzard_pos_0}

#def blizzard_at(turn):
#    try:
#        return blizzard_pos[turn]
#    else:
#        pre = blizzard_at(turn-1)
#        bl = [blizzard_next(b) for b in pre]
#        blizzards[turn] = bl
#        return bl

#turns = 1
#while True:
#    turns += 1
#    if turns >= h+w-2:
#        # try to find a path with this amount of turns

def bfs():
    #prev = {((1, 0), 0): (()}
    prev = {}
    unvisited = [((1,0), 0)]
    visited = set()

    while unvisited:
        state = unvisited.pop(0)
        if state in visited:
            continue
        visited.add(state)
        pos, turn = state
        print('turn', turn, len(unvisited))
        #print(unvisited[:50])
        try:
            bl_pos = blizzard_pos[turn+1]
        except KeyError:
            print('calculating blizzards at turn', turn+1)
            pre = blizzards[turn]
            bl = [blizzard_next(b) for b in pre]
            blizzards[turn+1] = bl
            bl_pos = set(pos for pos, d in bl)
            blizzard_pos[turn+1] = bl_pos

        for delta in ((0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)):
            q = a(pos, delta)
            if q[0] < 0 or q[1] < 0:
                continue
            if q not in walls and q not in bl_pos:
                tmp = (q, turn+1)
                if q == end:
                    path = [tmp, state]
                    while state in prev:
                        state = prev[state]
                        path.append(state)
                    path.reverse()
                    return path
                elif tuple(tmp) not in visited and tmp not in unvisited:
                    prev[tmp] = state
                    unvisited.append(tmp)

def print_turn(pos, turn):
    print('turn', turn)
    bl = blizzards[turn]
    for y in range(h):
        for x in range(w):
            if pos == (x, y):
                print('E', end='')
                continue
            if (x, y) in walls:
                print('#', end='')
                continue
            bs = [(p, d) for (p, d) in bl if p == (x, y)]
            if len(bs) == 1:
                print(bs[0][1], end='')
            elif bs:
                print(len(bs), end='')
            else:
                print('.', end='')
        print()

if __name__ == "__main__":
    path = bfs()
    #for pos, turn in path:
    #    print_turn(pos, turn)
    print(path)

