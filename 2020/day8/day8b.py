#!/usr/bin/env python3

with open('input') as f:
    inp = f.read().strip().split('\n')

def run(inp):
    pc = 0
    acc = 0
    visited = set()
    while True:
        if pc >= len(inp):
            #print('terminated', acc, pc)
            return acc
        if pc in visited:
            #print('loop detected', acc, pc)
            return None
        visited.add(pc)
        op, vs = inp[pc].split()
        #print(pc, op, vs)
        v = int(vs)
        if op == 'jmp':
            pc += v
        elif op == 'acc':
            acc += v
            pc += 1
        elif op == 'nop':
            pc += 1

for i, inst in enumerate(inp):
    op, vs = inst.split()
    tmp = list(inp)
    if op == 'jmp':
        tmp[i] = 'nop +0'
    elif op == 'nop':
        tmp[i] = 'jmp '+vs
    else:
        continue
    r = run(tmp)
    if r is not None:
        print('yay', r)
        break

