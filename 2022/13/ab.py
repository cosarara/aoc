#!/usr/bin/env python3

def cmp(a, b):
    #print("checking", a, b)
    if type(a) == list and type(b) == int:
        return cmp(a, [b])
    elif type(a) == int and type(b) == list:
        return cmp([a], b)
    elif type(a) == int and type(b) == int:
        #print("comparing ints", a, b)
        return b-a
    else: # type(a) == list and type(b) == list:
        if not a and not b:
            #print("empty, keep going")
            return 0
        if a and not b:
            #print("right ran out first, not in order")
            return -1
        if not a:
            #print("left ran out first, in order")
            return 1
        x = cmp(a[0], b[0])
        #print("compared first item:", x, a[0], b[0])
        if x < 0:
            return x
        if x > 0:
            return x
        #print("equal, recursing")
        return cmp(a[1:], b[1:])

def work(inp):
    pairs = [p.split('\n') for p in inp.strip().split('\n\n')]
    return [i+1 for i, (a, b) in enumerate(pairs) if cmp(eval(a), eval(b)) >= 0]

import functools
def work2(inp):
    packets = [eval(p) for p in inp.strip().split('\n') if p]+[[[2]], [[6]]]
    return sorted(packets, key=functools.cmp_to_key(lambda a, b: -cmp(a,b)))

import sys
inp = sys.stdin.read()
print("part a", sum(work(inp)))
l = work2(inp)
print("part b", (l.index([[2]])+1)*(l.index([[6]])+1))
