#!/usr/bin/env python3
import sys
import re

target = 2000000
#target = 10

seen = set()
beacons = set()
for line in sys.stdin:
    x, y, a, b = (int(n) for n in re.match(
        r'.*x=(-?\d+), y=(-?\d+).*x=(-?\d+), y=(-?\d+).*',
        line).groups())
    #print(x, y, a, b)

    if b == target:
        beacons.add(a)

    dist = abs(x-a)+abs(y-b)
    #for xx in range(x-dist, x+dist+1):
    #    d = abs(x - xx)
    #    for yy in range(y-dist+d, y+dist-d+1):
    #        seen.add((xx, yy))
    if y-dist <= target <= y+dist:
        #for yy in range(y-dist+d, y+dist-d+1):
        yy = target
        d = abs(y - yy)
        for xx in range(x-dist+d, x+dist-d+1):
            if yy == target:
                seen.add(xx)
#for y in range(-5, 23):
#for y in range(9, 12):
#    for x in range(-5, 28):
#        if (x, y) in beacons:
#            print('B', end='')
#        elif (x, y) in seen:
#            print('#', end='')
#        else:
#            print('.', end='')
#    print()
print(len(seen)-len(beacons))
