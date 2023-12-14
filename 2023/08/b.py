import sys
from itertools import cycle

with open(sys.argv[1]) as f:
    text = f.read().strip().split('\n')

instructions = text[0]
map = {}
for node_line in text[2:]:
    a = node_line[0:3]
    b = node_line[7:10]
    c = node_line[12:15]
    map[a] = (b, c)

nodes = [n for n in map if n[2] == "A"]
inst = cycle(instructions)
steps = 0
while [n for n in nodes if n[2] != "Z"]:
    dir = 0 if next(inst) == "L" else 1
    nodes = [map[n][dir] for n in nodes]
    #print(nodes)
    steps += 1

print(steps)
