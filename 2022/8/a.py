#!/usr/bin/env python3

def strgrid(grid):
    return('\n'.join([''.join(row) for row in grid]))

def top(grid, coord_transform=lambda x, y: (x, y)):
    visible = set()
    for x, highest in enumerate(grid[0]):
        for y, row in enumerate(grid):
            tree = grid[y][x]
            if y==0 or tree > highest:
                visible.add(coord_transform(x, y))
                highest = tree
    return visible

def visible(inp):
    grid = inp.strip().split('\n')
    w = len(grid[0])
    h = len(grid)
    # go around and mark the seen trees
    visible = top(grid)
    # bottom
    visible |= top(list(reversed(grid)), lambda x, y: (x, h-y-1))
    # left
    transposed = [[grid[x][y] for x, _ in enumerate(row)]
                  for y, row in enumerate(grid)]
    visible |= top(transposed, lambda x, y: (y, x))
    # right
    visible |= top(list(reversed(transposed)), lambda x, y: (w-y-1, x))
    return len(visible)

with open('example') as f:
    ex = f.read()

assert visible(ex) == 21

with open('input') as f:
    inp = f.read()

print(visible(inp))
