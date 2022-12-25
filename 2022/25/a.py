c2d = lambda c: (
    -1 if c == '-' else
    -2 if c == '=' else
    int(c))

s2d = lambda s: sum(c2d(c) * 5**(len(s)-1-n) for n,c in
                    enumerate(s.strip()))

import sys
t = sum(s2d(s) for s in sys.stdin.read().strip().split())
print(t)

def d2s(t):
    if t == 0:
        return '0'
    carry = 0
    tmp = t
    pos = 1
    o = ''
    while tmp:
        r = tmp%5
        #print('r', r, tmp, tmp*5**(pos-1), pos)
        if r == 3:
            o = '='+o
            tmp += 2
            carry = 1
        elif r == 4:
            tmp += 1
            o = '-'+o
            carry = 1
        else:
            o = str(r)+o
            tmp -= r
            carry = 0
        tmp //= 5
        pos += 1
        #print('o', o, tmp)
    return o

for i in list(range(11)) + [2022, 12345, 314159265]:
    print('TEST', i, d2s(i))
    assert(i == s2d(d2s(i)))

print(d2s(t))

