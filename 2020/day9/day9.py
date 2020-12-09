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

def find_sum(i):
    for j in range(2, len(xs)-i):
        r = xs[i:i+j]
        #print(i, j, r[:5])
        s = sum(r)
        if s > target:
            return None
        if s == target:
            return r

for i in range(len(xs)):
    r = find_sum(i)
    if r is not None:
        print('found', r, min(r)+max(r))
        break

