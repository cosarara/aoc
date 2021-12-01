with open("input.txt") as f:
    c = [int(x) for x in f.read().split("\n") if x]
#print(c)
c.reverse()
prev = c.pop()
count = 0
while c:
    curr = c.pop()
    print(prev, curr)
    if curr > prev:
        count += 1
    prev = curr
print(count, hex(count))
