ex = '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''.split('\n')
ex = [list(l) for l in ex]

def ray(grid, x, y, dx, dy):
    depth = 1
    try:
        while y+depth*dy >= 0 and x+depth*dx >= 0:
            c = grid[y+depth*dy][x+depth*dx]
            if c == '#':
                return 1
            if c == 'L':
                return 0
            depth += 1
        return 0
    except IndexError:
        return 0

def step(grid):
    ngrid = [list(r) for r in grid] #copy
    for y, l in enumerate(grid):
        for x, c in enumerate(l):
            if c == '.':
                continue
            adj = 0
            adj += ray(grid, x, y, -1, 0)
            adj += ray(grid, x, y, -1, 1)
            adj += ray(grid, x, y, -1, -1)
            adj += ray(grid, x, y, 1, 0)
            adj += ray(grid, x, y, 1, 1)
            adj += ray(grid, x, y, 1, -1)
            adj += ray(grid, x, y, 0, -1)
            adj += ray(grid, x, y, 0, 1)
            if adj == 0:
                ngrid[y][x] = '#'
            elif adj >= 5:
                ngrid[y][x] = 'L'
    return ngrid

def find(p):
    #print('\n'.join([''.join(l) for l in p]))
    #print()
    for i in range(10000):
        n = step(p)
        #print('\n'.join([''.join(l) for l in n]))
        #print()
        if n == p:
            print('\n'.join([''.join(l) for l in n]))
            print(sum([1 if c == '#' else 0 for l in n for c in l]))
            break
        p = n
    else:
        print('not found')

find(ex)

with open('input') as f:
    inp = f.read().strip().split('\n')
    inp = [list(l) for l in inp]

find(inp)
