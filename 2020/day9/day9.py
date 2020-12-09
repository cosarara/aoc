#!/usr/bin/env python3

with open('input') as f:
    xs = [int(x) for x in f.read().strip().split('\n')]

with open('example') as f:
    ex = [int(x) for x in f.read().strip().split('\n')]

def test(y, preamble):
    pset = set(preamble)
    for x in preamble:
        if x!=y and y-x in pset:
            return True
    return False

print('example')
for i in range(5, len(ex)):
    preamble = xs[i-5:i]
    y = xs[i]
    print(i, preamble, y)
    if not test(y, preamble):
        print(y)
        break

print('real')
for i in range(25, len(xs)):
    preamble = xs[i-25:i]
    y = xs[i]
    if not test(y, preamble):
        print(y)
        break

print('part b')
target = y

s = 0
e = 1
x = xs[0]
while e < len(xs):
    if x == target:
        r = xs[s:e]
        print('found', r, min(r)+max(r))
        break
    x += xs[e]
    e += 1
    while x > target:
        x -= xs[s]
        s += 1

