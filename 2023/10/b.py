import sys

with open(sys.argv[1]) as f:
    grid = f.read().strip().split("\n")

for y, line in enumerate(grid):
    if "S" in line:
        start = (line.find("S"), y)
        break

def adjacent(x, y):
    return ((x+1, y, 'e'), (x-1, y, 'w'), (x, y+1, 's'), (x, y-1, 'n'))

outer_connections = {
    'e': 'LF-',
    'w': 'J7-',
    's': '7F|',
    'n': 'LJ|'
}

connections = {
    '-': 'ew',
    '|': 'ns',
    'F': 'se',
    'L': 'ne',
    'J': 'nw',
    '7': 'sw',
}

opposite = {
    'e': 'w',
    'w': 'e',
    's': 'n',
    'n': 's'
}

def find_start(x, y):
    return [(x, y, dir) for x, y, dir in adjacent(x, y)
            if grid[y][x] in outer_connections[opposite[dir]]]

def find_next(x, y):
    shape = grid[y][x]
    return [(x0, y0) for x0, y0, dir in adjacent(x, y)
            if dir in connections[shape]]

forward, backward = find_start(*start)
d1, d2 = forward[2], backward[2]

# replace the stupid S by the proper sign
for sym in 'LJ7F|-':
    if d1 in connections[sym] and d2 in connections[sym]:
        print('S should be a', sym)
        x, y = start
        grid[y] = grid[y].replace('S', sym)
        break

forward = forward[:2]
backward = backward[:2]

print(forward, backward)
current = forward
def visit_from(current):
    distance = 1
    visited = set((start,))
    while True:
        visited.add(current)
        conns = find_next(*current)
        unvisited = [p for p in conns if p not in visited]
        #print(current, conns, unvisited)
        if not unvisited:
            #print(conns == [backward])
            break
        current = unvisited[0]
        distance += 1
    return visited

visited = visit_from(forward)

def inside(x, y):
    if (x, y) in in_path:
        return False

    # cast an horizontal ray and count how many times we cross the
    # path
    crossed = 0
    for x0 in range(x):
        # we are going to pretend we go under - and J and L so we don't cross it
        if (x0, y) in in_path and grid[y][x0] in 'F7|':
            crossed += 1
    return crossed % 2 == 1

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

tiles_inside = 0
for y, line in enumerate(grid):
    crossed = 0
    for x, c in enumerate(line):
        if (x, y) in visited:
            if grid[y][x] in 'F7|':
                crossed += 1
            print(color.RED + c + color.END, end='')
        #elif inside(x, y):
        elif crossed % 2:
            print('I', end='')
            tiles_inside += 1
        else:
            print('O', end='')
    print()

print()
print(tiles_inside)
