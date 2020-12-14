t = 1003055
inp = '37,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,433,x,x,x,x,x,x,x,23,x,x,x,x,x,x,x,x,17,x,19,x,x,x,x,x,x,x,x,x,29,x,593,x,x,x,x,x,x,x,x,x,x,x,x,13'
inp = inp.split(',')
inp = [int(a) for a in inp if a != 'x']
print(inp)
d = {k: 0 for k in inp}
done = False
while not done:
    done = True
    for k, v in d.items():
        if v < t:
            d[k] += k
            done = False


mink = inp[0]
for k, v in d.items():
    if v < d[mink]:
        mink = k
print(mink, d[mink], (d[mink] - t) * mink)
