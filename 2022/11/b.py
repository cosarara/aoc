#!/usr/bin/env python
import sys
from pprint import pprint

text = sys.stdin.read()
tmonkeys = text.split('\n\n')
pprint(tmonkeys)

class Monkey():
    mid = 0
    items = []
    op = lambda x: x
    test_div_by = 1
    monkey_true = 1
    monkey_false = 1
    inspections = 0
    divider = 1

    def turn(self):
        self.inspections += len(self.items)
        for item in self.items:
            new = self.op(item) % divider
            if new % self.test_div_by == 0:
                monkeys[self.monkey_true].receive(new)
            else:
                monkeys[self.monkey_false].receive(new)
        self.items = []

    def receive(self, item):
        self.items.append(item)

def make_op(op_parts):
    operator = op_parts[1]
    b = op_parts[2]
    if operator == "+":
        if b == "old":
            return lambda x: x+x
        b = int(b)
        return lambda x: x+b
    elif operator == "*":
        if b == "old":
            return lambda x: x*x
        b = int(b)
        return lambda x: x*b
    else:
        raise Exception('operator not understood', operator)

monkeys = []
for tmonkey in tmonkeys:
    monkey = Monkey()
    monkey.mid = len(monkeys)
    lines = tmonkey.split('\n')
    monkey.items = [int(x.strip()) for x in
                    lines[1].split(':')[1].strip().split(',')]
    text_op = lines[2].split('=')[1].strip()
    op_parts = text_op.split()
    monkey.op = make_op(op_parts)
    monkey.test_div_by = int(lines[3].split(' ')[-1])
    monkey.monkey_true = int(lines[4].split(' ')[-1])
    monkey.monkey_false = int(lines[5].split(' ')[-1])
    monkeys.append(monkey)

print([m.test_div_by for m in monkeys])
from functools import reduce
divider = reduce(lambda a, b: a*b, [m.test_div_by for m in monkeys],
                 1)
for monkey in monkeys:
    monkey.divider = divider

for turn in range(10000):
    for monkey in monkeys:
        monkey.turn()
    if turn % 100 == 0:
        print(turn)
        for monkey in monkeys:
            print(monkey.mid, monkey.items)

print('inspection counts')
for monkey in monkeys:
    print(monkey.mid, monkey.inspections)

a, b = sorted([m.inspections for m in monkeys])[-2:]
print(a*b)
