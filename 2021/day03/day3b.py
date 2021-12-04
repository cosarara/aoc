with open('input.txt') as f:
    a = f.read().strip().split('\n')

t = a
for bit in range(12):
    ones = sum([int(v[bit]) for v in t])
    good = '0'
    if ones >= len(t)/2:
        good = '1'
    print(bit, len(t), ones, good)
    t = [v for v in t if v[bit] == good]
    #print(t)
    if len(t) == 1:
        break

s = a
for bit in range(12):
    ones = sum([int(v[bit]) for v in s])
    good = '1'
    if ones >= len(s)/2:
        good = '0'
    print(bit, len(s), ones, good)
    s = [v for v in s if v[bit] == good]
    if len(s) == 1:
        break
print(t, s)
o = int(t[0], 2)
co2 = int(s[0], 2)
print(o, co2, o*co2)
