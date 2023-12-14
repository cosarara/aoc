import sys
from itertools import cycle

with open(sys.argv[1]) as f:
    text = f.read().strip().split('\n')

instructions = text[0]
nodes = {}
for node_line in text[2:]:
    a = node_line[0:3]
    b = node_line[7:10]
    c = node_line[12:15]
    nodes[a] = (b, c)

node = 'AAA'
inst = cycle(instructions)
steps = 0
while node != 'ZZZ':
    dir = next(inst)
    a, b = nodes[node]
    print(node, a, b, dir)
    if dir == "R":
        node = b
    elif dir == "L":
        node = a
    steps += 1

print(steps)
