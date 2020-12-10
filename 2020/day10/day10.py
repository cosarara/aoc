from functools import cache

with open('example') as f:
    ex = [int(i) for i in f.read().strip().split('\n')]
    ex.sort()

with open('input') as f:
    inp = [int(i) for i in f.read().strip().split('\n')]
    inp.sort()

def do(inp):
    prev = inp[0]
    counts = {0: 0, 1: 0, 2: 0, 3: 1}
    counts[prev] += 1
    for x in inp[1:]:
        diff = x - prev
        prev = x
        if diff in counts:
            counts[diff] += 1
        else:
            print("uh diff is", diff)
            break
    print(counts)
    print(counts[1] * counts[3])

# memoization is great, slow suddenly is fast
@cache
def arrangements_slow(inp):
    if len(inp) == 1:
        return 1
    curr = inp[0]
    #the next will always be ok, but what about the others
    possibs = arrangements_slow(inp[1:])
    try:
        if inp[2] - curr <= 3:
            possibs += arrangements_slow(inp[2:])
        if inp[3] - curr <= 3:
            possibs += arrangements_slow(inp[3:])
    except IndexError:
        pass
    return possibs

# ok my brain can't actually come up with
# a fast algorithm
def arrangements(inp):
    if len(inp) == 1:
        return 1
    curr = inp[0]
    #the next will always be ok, but what about the others
    #possibs = arrangements(inp[1:])
    try:
        if inp[3] - curr <= 3:
            x = arrangements(inp[3:])
            return x + 2*x + 4*x
    except IndexError:
        pass
    try:
        if inp[2] - curr <= 3:
            return 2 * arrangements(inp[2:])
    except IndexError:
        pass
    return arrangements(inp[1:])

do(ex)
do(inp)

def t(i):
    print(arrangements_slow(tuple(i)), arrangements(i))
(t([4,5,6]))
(t([3,4,5,6]))
(t([2,3,4,5,6]))
(t([0,1,2,3,4,5,6]))
(t([4,5]))
(t([3,4,5]))
(t([2,3,4,5]))
(t([0,1,2,3,4,5]))
#t([0]+ex)
print(arrangements_slow(tuple([0]+ex)))
print(arrangements_slow(tuple([0]+inp)))
