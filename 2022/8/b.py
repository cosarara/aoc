#!/usr/bin/env python3

def score(grid, x0, y0):
    u,d,r,l = 0,0,0,0
    base = grid[y0][x0]
    w = len(grid[0])
    h = len(grid)
    for x in range(x0-1, -1, -1):
        l += 1
        if grid[y0][x] >= base:
            break
    for x in range(x0+1, w):
        r += 1
        if grid[y0][x] >= base:
            break
    for y in range(y0-1, -1, -1):
        u += 1
        if grid[y][x0] >= base:
            break
    for y in range(y0+1, h):
        d += 1
        if grid[y][x0] >= base:
            break

    return u*d*r*l

def best(inp):
    grid = inp.strip().split('\n')
    w = len(grid[0])
    h = len(grid)
    return max(score(grid, x, y) for x in range(1,w-1) for y in
               range(1,h-1))

with open('example') as f:
    ex = f.read()

assert best(ex) == 8

with open('input') as f:
    inp = f.read()

print(best(inp))
