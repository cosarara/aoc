#!/usr/bin/env python

def a(inp):
    a,b,c = inp[0:3]
    for i, d in enumerate(inp[3:]):
        if len(set((a,b,c,d))) == 4:
            print(i, a, b, c, d)
            return i+4
        a,b,c = b,c,d

assert a('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 7
assert a('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
assert a('nppdvjthqldpwncqszvftbrmjlhg') == 6
assert a('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 10
assert a('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11

with open('input') as f:
    x = f.read()
print('part a:', a(x))

def b(inp, l):
    for i, _ in enumerate(inp[l:]):
        roll = inp[i:i+l]
        if len(set(roll)) == l:
            print(roll)
            return i+l

assert b('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4) == 7
assert b('bvwbjplbgvbhsrlpgdmjqwftvncz', 4) == 5
assert b('nppdvjthqldpwncqszvftbrmjlhg', 4) == 6
assert b('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4) == 10
assert b('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4) == 11
assert b('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14) == 19
assert b('bvwbjplbgvbhsrlpgdmjqwftvncz', 14) == 23

print('part b:', b(x, 14))
