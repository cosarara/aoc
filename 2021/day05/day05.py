with open('input.txt') as f:
    strings = f.read().strip().split('\n')

from collections import defaultdict
world = defaultdict(lambda: 0)
for s in strings:
    src, dest = s.split(' -> ')
    a, b = src.split(',')
    c, d = dest.split(',')
    a, b, c, d = (int(x) for x in (a, b, c, d))
    if a == c:
        for y in range(min(b, d), max(b, d)+1):
            world[(a, y)] += 1
    if b == d:
        for x in range(min(a, c), max(a, c)+1):
            world[(x, b)] += 1

print(sum(1 for point in world.values()
          if point>=2))

# part b
world = defaultdict(lambda: 0)
for s in strings:
    src, dest = s.split(' -> ')
    a, b = src.split(',')
    c, d = dest.split(',')
    a, b, c, d = (int(x) for x in (a, b, c, d))
    if a == c:
        for y in range(min(b, d), max(b, d)+1):
            world[(a, y)] += 1
    elif b == d:
        for x in range(min(a, c), max(a, c)+1):
            world[(x, b)] += 1
    else:
        #print(s)
        # always left to right
        (a, b), (c, d) = sorted([(a, b), (c, d)])
        #print(c, a)
        for n in range(c - a + 1):
            if b < d: # down
                #print(a+n, b+n)
                world[(a+n, b+n)] += 1
            else: # up
                #print(a+n, c+n)
                world[(a+n, b-n)] += 1

print(sum(1 for point in world.values()
          if point>=2))

#for y in range(10):
#    for x in range(10):
#        print(world[x, y], end=' ')
#    print('')
