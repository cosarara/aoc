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
    return [(x, y) for x, y, dir in adjacent(x, y)
            if grid[y][x] in outer_connections[opposite[dir]]]

def find_next(x, y):
    shape = grid[y][x]
    return [(x0, y0) for x0, y0, dir in adjacent(x, y)
            if dir in connections[shape]]

forward, backward = find_start(*start)
print(forward, backward)
current = forward
distances = {forward: 1, backward: 1}
def visit_from(current):
    distance = 1
    visited = set((start,))
    while True:
        visited.add(current)
        conns = find_next(*current)
        unvisited = [p for p in conns if p not in visited]
        print(current, conns, unvisited)
        if not unvisited:
            print(conns == [backward])
            break
        current = unvisited[0]
        distance += 1
        if current not in distances or distance < distances[current]:
            distances[current] = distance
        else:
            break
visit_from(forward)
visit_from(backward)

print(distances)
print(max(distances, key=lambda x: distances[x]))
print(max(distances.values()))
