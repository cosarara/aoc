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
for line in sys.stdin:
    if not line.strip():
        continue
    cube = tuple(int(a) for a in line.strip().split(','))
    cubes.add(cube)

surface = 0
for cube in cubes:
    for side in sides(cube):
        if side not in cubes:
            surface += 1
print(surface)
