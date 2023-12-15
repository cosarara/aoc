import sys

with open(sys.argv[1]) as f:
    grid = f.read().strip().split('\n')

outgrid = []
for row in grid:
    outrow = ""
    for x, c in enumerate(row):
        if not '#' in (grid[y][x] for y in range(len(grid))):
            outrow += ".."
        else:
            outrow += c
    times = 1
    if not '#' in row:
        times = 2
    for i in range(times):
        outgrid.append(outrow)

grid = outgrid
#print('\n'.join(grid))

galaxies = []
for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == '#':
            galaxies.append((x, y))

result = 0
for n1, g1 in enumerate(galaxies):
    for n2, g2 in enumerate(galaxies):
        if g1 == g2:
            continue
        x1, y1 = g1
        x2, y2 = g2
        distance = abs(x1 - x2) + abs(y1 - y2)
        print(n1+1, n2+1, distance)
        result += distance

print(result / 2)
