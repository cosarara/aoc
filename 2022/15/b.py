#!/usr/bin/env python3
import sys
import re

limit = 4_000_000
#limit = 20
def valid(point):
    x, y = point
    return 0 <= x <= limit and 0 <= y <= limit

seen = set()
beacons = set()
sensors = [] # (x, y, radius)
edges = []

outer_lines_up = []
outer_lines_down = []

for n, line in enumerate(sys.stdin):
    x, y, a, b = (int(n) for n in re.match(
        r'.*x=(-?\d+), y=(-?\d+).*x=(-?\d+), y=(-?\d+).*',
        line).groups())
    dist = abs(x-a)+abs(y-b)
    sensors.append((x, y, dist))
    p = (x, y-dist-1) # bottom (displayed top)
    q = (x, y+dist+1) # top (displayed bot)
    r = (x+dist+1, y) # right
    s = (x-dist-1, y) # left

    outer_lines_up.append((p,r)) # bottom->right
    outer_lines_down.append((s,p)) # left->bottom
    outer_lines_down.append((q,r)) # top->right
    outer_lines_up.append((s,q)) # left->top

    #if n in [0, 1]:
    #for yy in range(y-dist, y+dist+1):
    #    d = abs(y - yy)
    #    for xx in range(x-dist+d, x+dist-d+1):
    #        seen.add((xx, yy))

def intersect(a, b): # a goes up, b goes down
    p, q = a # positive slope
    r, s = b # negative slope
    if p in (r, s):
        return p
    if q in (r, s):
        return q

    # the line from p to q is y=x*m+n
    # ma is  1
    # mb is -1
    # y = x * m + n
    # ya = xa * 1 + nb
    # ya - xa = na
    # yb = - xb + nb
    # yb + xb = nb
    # na is p.y - p.x
    na = p[1] - p[0]
    # nb is r.y - r.x
    nb = r[0] + r[1]
    #   y =  x+na
    # -(y = -x+nb)
    #   0 = 2x+(na-nb)
    # -2x = na-nb
    #   x = (nb-na)/2
    x = (nb-na)//2
    y = x+na
    return (x, y)

def in_range(sensor, point):
    x, y, radius = sensor
    xx, yy = point
    distance = abs(x-xx)+abs(y-yy)
    return distance <= radius

for up in outer_lines_up:
    found = False
    for down in outer_lines_down:
        p = intersect(up, down)
        #print('intersection', 'up', up, 'down', down, p)
        if not valid(p):
            continue
        for sensor in sensors:
            if in_range(sensor, p):
                break
        else:
            print('found', p)
            x, y = p
            print(x*limit+y)
            found = True
            break
    if found:
        break

