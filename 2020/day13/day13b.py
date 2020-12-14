inp = '37,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,433,x,x,x,x,x,x,x,23,x,x,x,x,x,x,x,x,17,x,19,x,x,x,x,x,x,x,x,x,29,x,593,x,x,x,x,x,x,x,x,x,x,x,x,13'

# busquem i tal que
# tots els X[n] son múltiples d'X[0]*i + T[n]
#i = 1
#while True:
#    start = pairs[0][0] * i
#    #print('start', start)
#    for base, target in pairs[1:]:
#        if (start + target) % start != 0:
#            break
#    else:
#        print('gochu', start, i)
#
#
#    i+=1

# per passos
# si busquem quan passa que arribi el 37 i 1 min més tard el 41:
# passa a 37 * 31 = 1147, 41 * 28 = 1148
# i torna a passar a
# 37 * (41 + 31) = 2664
# 41 * (37 + 28) = 2665
# i a
# 37 * (n*41 + 31)
# 41 * (n*37 + 28)

# per tant puc tractar 37 * 41 com una unitat i buscar el següent cas?

def find(f, base, target):
    for x in range(1000):
        if f(x)%base == target%base:
            return x

def nextf(f, base, target):
    t = find(f, base, target)
    return lambda x: f(x*base+t)

def do(inp):
    inp = inp.split(',')
    pairs = [(int(a), n) for n, a in enumerate(inp) if a != 'x']
    f = lambda x: x
    for base, target in pairs:
        target = (base - target) % base
        print(f(0))
        f = nextf(f, base, target)
    t = f(0)
    print('diffs:')
    for p, d in pairs:
        print(p, p-t%p, d%p)
    return t

print(do('7,13,x,x,59,x,31,19'))
print(do(inp))
