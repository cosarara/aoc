import sys

with open(sys.argv[1]) as f:
    patterns = f.read().strip('\n').split('\n\n')

patterns = [p.split() for p in patterns]
#print(patterns)

def find_mirror(p):
    for y in range(1, len(p) - 1):
        l = min(y, len(p) - y)
        #print(y, ': length', l, ':', y-l, 'to', y, 'to', y+l)
        #if y == 9:
        #    print(p[y-l:y])
        #    print()
        #    print(list(reversed(p[y:y+l])))
        #    print()
        #    print(p[y-l:y] == list(reversed(p[y:y+l])))
        if p[y-l:y] == list(reversed(p[y:y+l])):
            return y
    return None

def find_vertical_mirror(p):
    lines = []
    for x in range(len(p[0])):
        lines.append(''.join(l[x] for l in p))

    print('\n' + '\n'.join(f'{x+1:2} '+l for x, l in enumerate(lines)) + '\n')
    return find_mirror(lines)

total = 0
for p in patterns:
    print('\n' + '\n'.join(f'{x+1:2} '+l for x, l in enumerate(p)) + '\n')
    h = find_mirror(p)
    if h:
        print('horizontal mirror at', h)
        total += h * 100
    v = find_vertical_mirror(p)
    if v:
        total += v
        #print(" "*(v-1)+"^^")
        print('vertical mirror at', v)

    print()

print(total)
