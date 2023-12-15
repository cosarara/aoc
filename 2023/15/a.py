def hash(s):
    o = 0
    for c in s:
        o += ord(c)
        o *= 17
        o %= 256
    return o

#print(hash('HASH'))
import sys
with open(sys.argv[1]) as f:
    steps = f.read().replace('\n', '').split(',')
print(sum(hash(s) for s in steps))
