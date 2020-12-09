#!/usr/bin/env python3

with open('input') as f:
    inp = f.read().split('\n')

pc = 0
acc = 0
visited = set()
while True:
    if pc in visited:
        print('end', acc, pc)
        break
    visited.add(pc)
    op, vs = inp[pc].split()
    print(pc, op, vs)
    v = int(vs)
    if op == 'jmp':
        pc += v
    elif op == 'acc':
        acc += v
        pc += 1
    elif op == 'nop':
        pc += 1
