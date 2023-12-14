import sys
from itertools import cycle
from math import lcm

with open(sys.argv[1]) as f:
    text = f.read().strip().split('\n')

instructions = text[0]
map = {}
for node_line in text[2:]:
    a = node_line[0:3]
    b = node_line[7:10]
    c = node_line[12:15]
    map[a] = (b, c)

def cycles(n):
    inst = cycle(instructions)
    steps = 0
    while n[2] != "Z":
        dir = 0 if next(inst) == "L" else 1
        n = map[n][dir]
        steps += 1
    return steps

node_cycles = [cycles(n) for n in map if n[2] == "A"]
print(node_cycles)
print(lcm(*node_cycles))
