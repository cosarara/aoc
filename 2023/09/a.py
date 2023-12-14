import sys

def derive(xs):
    out = []
    for n, _ in enumerate(xs[:-1]):
        a, b = xs[n], xs[n+1]
        out.append(b-a)
    return out

def value(xs):
    derived = derive(xs)
    if not [x for x in derived if x != 0]: # if derived is all zeroes
        return xs[0] # it doesn't matter they are all the same
    else:
        return xs[-1] + value(derived)

result = 0
with open(sys.argv[1]) as f:
    for line in f:
        v = value([int(a) for a in line.split()])
        print(v)
        result += v
print(result)
