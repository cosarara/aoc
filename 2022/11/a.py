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

    def turn(self):
        for item in self.items:
            self.inspections += 1
            #print(f'monkey {self.mid} inspects item with worry lvl of {item}')
            new = self.op(item)
            #print(f'worry level increases to {new}')
            new //= 3
            if new % self.test_div_by == 0:
                #print(f'divisible by {self.test_div_by}')
                monkeys[self.monkey_true].receive(new)
            else:
                #print(f'not divisible by {self.test_div_by}')
                monkeys[self.monkey_false].receive(new)
        self.items = []

    def receive(self, item):
        self.items.append(item)

monkeys = []
for tmonkey in tmonkeys:
    monkey = Monkey()
    monkey.mid = len(monkeys)
    lines = tmonkey.split('\n')
    monkey.items = [int(x.strip()) for x in
                    lines[1].split(':')[1].strip().split(',')]
    text_op = lines[2].split('=')[1].strip()
    op_parts = text_op.split()
    def op(old, op_parts=op_parts):
        a = op_parts[0]
        operator = op_parts[1]
        b = op_parts[2]
        a = old if a == "old" else int(a)
        b = old if b == "old" else int(b)
        #print(a, operator, b)
        return {"+": lambda a, b: a+b,
                "*": lambda a, b: a*b}[operator](a, b)
    monkey.op = op
    monkey.test_div_by = int(lines[3].split(' ')[-1])
    monkey.monkey_true = int(lines[4].split(' ')[-1])
    monkey.monkey_false = int(lines[5].split(' ')[-1])
    monkeys.append(monkey)

for turn in range(20):
    print('turn', turn)
    for monkey in monkeys:
        monkey.turn()

    print('items at end of turn')
    for monkey in monkeys:
        print(monkey.mid, monkey.items)

print('inspection counts')
for monkey in monkeys:
    print(monkey.mid, monkey.inspections)

a, b = sorted([m.inspections for m in monkeys])[-2:]
print(a*b)
