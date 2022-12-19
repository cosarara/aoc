def sides(cube):
    x, y, z = cube
    return (
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    )

import sys
cubes = set()
maxc = 0
for line in sys.stdin:
    if not line.strip():
        continue
    cube = tuple(int(a) for a in line.strip().split(','))
    maxc = max(maxc, *cube)
    cubes.add(cube)

maxc += 1
print(maxc)

for y in range(maxc):
    for x in range(maxc):
        for z in range(maxc):
            if (x,y,z) in cubes:
                print('x', end='')
                break
        else:
            print(' ', end='')
    print()

visited = set()
outside = set()
to_visit = [(0,0,0)]

while to_visit:
    curr = to_visit.pop(0)
    if curr in visited:
        continue
    visited.add(curr)
    if curr not in cubes:
        outside.add(curr)
    for side in sides(curr):
        x, y, z = side
        if (x < -1 or x > maxc or
            y < -1 or y > maxc or
            z < -1 or z > maxc):
            continue
        if side not in cubes:
            to_visit.append(side)


surface = 0
for cube in cubes:
    for side in sides(cube):
        if side not in cubes and side in outside:
            surface += 1
        if side not in cubes and side not in outside:
            print(side)
print(surface)
