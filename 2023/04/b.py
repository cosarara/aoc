with open("input.txt") as f:
    lines = [l.strip('\n') for l in f]

def get_points(d):
    wins, haves = d.split(" | ")
    nwins = len(set(wins.split()) & set(haves.split()))
    return nwins

cache = {}
for line in lines:
    idpart, d = line.split(": ")
    _, id = idpart.split()
    id = int(id)
    points = get_points(d)
    refs = list(range(id+1, id+points+1))
    cache[id] = refs

print(cache)

values = {}
for key in reversed(cache.keys()):
    subcards = cache[key]
    val = 1
    for subcard in subcards:
        val += values[subcard]
    values[key] = val

#print(values)
print(sum(values.values()))
