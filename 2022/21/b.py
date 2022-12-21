import sys

ops = {}
for line in sys.stdin:
    name, etc = line.strip().split(": ")
    if name == "root":
        etc = etc.replace('+', '=')
    if name == 'humn':
        continue
    ops[name] = etc

big = ops["root"]
for i in range(len(ops)):
    oldbig = big
    for n, op in ops.items():
        big = big.replace(n, "("+op+")")
    if big == oldbig:
        break

print(big)


