#!/usr/bin/env python3

import sys
lines = [l.strip() for l in sys.stdin]
graph = {}

start = ()
goal = ()

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == 'S':
            start = (x, y)
        if char == 'E':
            goal = (x, y)
        outs = set()
        for xx, yy in ((x-1, y), (x+1, y),
                       (x, y-1), (x, y+1)):
            if xx >= 0 and yy >= 0:
                try:
                    out = lines[yy][xx]
                    if out == 'E':
                        if char == 'z':
                            outs.add((xx, yy))
                    elif char=='S' or ord(out) <= ord(char)+1:
                        outs.add((xx, yy))
                except IndexError:
                    pass
        graph[(x, y)] = outs

print(graph)

def walk(walked, bestlen=None):
    best = None
    if bestlen and bestlen < len(walked):
        return None
    if len(walked) % 50 == 0:
        print(len(walked))
    for node in graph[walked[-1]]:
        if node in walked:
            continue # don't walk in loops
        if node == goal:
            return walked+[node]
        path = walk(walked+[node], bestlen)
        if path and (not best or len(path) < len(best)):
            best = path
            bestlen = len(path)
            print('current best len', bestlen)
    return best

best = walk([start])
for node in best:
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if (x, y) == node:
                print('@', end="")
            else:
                print(char, end="")
        print()
    print()

print(best, len(best)-1)

