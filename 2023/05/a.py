with open("input.txt") as f:
    content = f.read()

sections = content.strip('\n').split('\n\n')
seeds = [int(s) for s in sections[0].split(': ')[1].strip().split()]
print(seeds)

maps = []
titles = []
for section in sections[1:]:
    lines = section.split('\n')
    titles.append(lines[0])
    ranges = []
    for line in lines[1:]:
        dst, src, length = [int(s) for s in line.split()]
        ranges.append((dst, src, length))
    maps.append(ranges)

#print(maps)
results = []
for seed in seeds:
    v = seed
    for title, map in zip(titles, maps):
        for dst, src, length in map:
            if src <= v <= src+length:
                #print(title)
                #print('using map', dst, src, length, 'for value', v,
                #      'in range [', src, '-', src+length, ']')
                #print('src', src, 'length', length, 'v', v)
                #print('mapping', v, 'to', dst + v - src)
                v = dst + v - src
                break
    results.append(v)
print(min(results))
