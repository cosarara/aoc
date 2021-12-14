def get_input(fn="input.txt"):
    with open(fn) as f:
        s = f.read().strip().split(',')
    return [int(x) for x in s]

def cost(crabs, x):
    return sum(abs(x-crab) for crab in crabs)

def part1():
    crabs = get_input("input.txt")
    miny = None
    minx = None
    for x in range(max(crabs)):
        y = cost(crabs, x)
        if miny is None or y < miny:
            miny = y
            minx = x
    print(miny, minx)

import functools

@functools.cache
def fuel(n):
    return sum(range(n+1))

def cost2(crabs, x):
    return sum(fuel(abs(x-crab)) for crab in crabs)

def part2():
    crabs = get_input("input.txt")
    miny = None
    minx = None
    for x in range(max(crabs)):
        y = cost2(crabs, x)
        if miny is None or y < miny:
            miny = y
            minx = x
    print(miny, minx)

if __name__ == "__main__":
    part1()
    part2()
