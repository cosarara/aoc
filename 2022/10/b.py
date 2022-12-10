#!/usr/bin/env python
import sys
instructions = list(sys.stdin)

READING=1
ADDING=2

state = READING
to_add = None
X = 1

# screen is 40x6
screen_cycle = 0

for cycle in range(1, 241):
    #print(cycle, X, cycle*X)
    if screen_cycle % 40 == 0:
        print()
    if screen_cycle%40 in [X-1, X, X+1]:
        print('#', end='')
    else:
        print('.', end='')
    screen_cycle += 1
    screen_cycle %= 240

    if state == READING:
        if not instructions:
            print('end of instructions')
            break
        inst = instructions.pop(0).strip()
        parts = inst.split(' ')
        op = parts[0]
        if op == "noop":
            pass
        elif op == "addx":
            to_add = int(parts[1])
            state = ADDING
        else:
            print(op)
            assert False
    elif state == ADDING:
        #print('adding', to_add)
        X += to_add
        state = READING
    else:
        print(state)
        assert False # unreachable
print()
