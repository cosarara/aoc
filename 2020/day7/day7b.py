from collections import defaultdict
import re
with open('input') as f:
    srules = f.read().split('\n')

# key must hold [(n, c)]
rules = defaultdict(list)
# example: vibrant lime bags contain 3 faded gold bags, 3 plaid aqua bags, 2 clear black bags.
line_exp = re.compile(r'(?P<outer>\w+ \w+) bags contain (?P<inner>((\d+) (\w+ \w+) bags?[,.] ?)+)')
colors_exp = re.compile(r'((\d+) (\w+ \w+) bags?[,.] ?)')
for l in srules:
    if 'no other bags' in l or not l:
        continue
    match = re.match(line_exp, l)
    inner = [(int(n), c) for (_, n, c) in re.findall(colors_exp, match['inner'])]
    rules[match['outer']] = inner

def rec(n, c):
    print(n, c)
    count = n
    for nn, cc in rules[c]:
        count += n*rec(nn, cc)
    return count
print(rec(1, 'shiny gold') - 1)
