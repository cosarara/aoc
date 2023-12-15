import sys

with open(sys.argv[1]) as f:
    patterns = f.read().strip('\n').split('\n\n')

patterns = [p.split() for p in patterns]
#print(patterns)

def one_smudge(a, b):
    diffs = 0
    for row_a, row_b in zip(a, b):
        for ca, cb in zip(row_a, row_b):
            if ca != cb:
                diffs += 1
                if diffs > 1:
                    return False
    return diffs == 1

def find_mirror(p):
    mirrors = []
    for y in range(1, len(p)):
        l = min(y, len(p) - y)
        if one_smudge(p[y-l:y], list(reversed(p[y:y+l]))):
            mirrors.append(y)
    if len(mirrors) > 1:
        print(mirrors)
        raise Exception("multiple mirrors")
    return mirrors[0] if mirrors else None

def transpose(p):
    lines = []
    for x in range(len(p[0])):
        lines.append(''.join(l[x] for l in p))
    return lines

total = 0
for p in patterns:
    h = find_mirror(p)
    v = find_mirror(transpose(p))
    print('\n' + '\n'.join(f'{x+1:2} '+l+('<' if h and x in (h-1, h) else '') for x, l in enumerate(p)))
    if v:
        total += v
        print(" "*3+" "*(v-1)+"^^")
        print(' '*3 + ''.join(str(i%10) for i in range(len(p[0]))))
        print('vertical mirror at', v)
    if h:
        print('horizontal mirror at', h)
        total += h * 100
    if not h and not v:
        print('nothing')

    print()

print(total)
