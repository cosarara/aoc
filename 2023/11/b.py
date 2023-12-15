import sys

with open(sys.argv[1]) as f:
    grid = f.read().strip().split('\n')

expansion = 1_000_000

emptyrows = []
emptycols = []
outgrid = []
for y, row in enumerate(grid):
    if not '#' in row:
        emptyrows.append(y)

for x in range(len(grid)):
    if not '#' in (grid[y][x] for y in range(len(grid))):
        emptycols.append(x)

print(emptycols, emptyrows)

galaxies = []
for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == '#':
            galaxies.append((x, y))

result = 0
for n1, g1 in enumerate(galaxies):
    for n2, g2 in enumerate(galaxies):
        if g1 == g2 or n1 > n2:
            continue
        x1, y1 = g1
        x2, y2 = g2
        x1, x2 = sorted((x1, x2))

        distance = abs(x1 - x2) + abs(y1 - y2)
        for x in range(x1, x2):
            if x in emptycols:
                #print("adjusting for column", x)
                distance += expansion - 1
        for y in range(y1, y2):
            if y in emptyrows:
                #print("adjusting for row", y)
                distance += expansion - 1
        print(n1+1, n2+1, distance)
        result += distance

print(result)
