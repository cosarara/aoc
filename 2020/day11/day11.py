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

def step(grid):
    ngrid = [list(r) for r in grid] #copy
    for y, l in enumerate(grid):
        for x, c in enumerate(l):
            if c == '.':
                continue
            adj = 0
            # top
            if y > 0:
                if grid[y-1][x] == '#':
                    adj += 1
                if x > 0 and grid[y-1][x-1] == '#':
                    adj += 1
                if x+1 < len(l) and grid[y-1][x+1] == '#':
                    adj += 1
            # bottom
            if y+1 < len(grid):
                if grid[y+1][x] == '#':
                    adj += 1
                if x > 0 and grid[y+1][x-1] == '#':
                    adj += 1
                if x+1 < len(l) and grid[y+1][x+1] == '#':
                    adj += 1
            # left
            if x > 0:
                if grid[y][x-1] == '#':
                    adj += 1
            # right
            if x+1 < len(l):
                if grid[y][x+1] == '#':
                    adj += 1
            if adj == 0:
                ngrid[y][x] = '#'
            elif adj >= 4:
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
