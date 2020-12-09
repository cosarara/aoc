from collections import defaultdict
import re
with open('input') as f:
    srules = f.read().split('\n')

# key can be held by [values]
rules = defaultdict(list)
# example: vibrant lime bags contain 3 faded gold bags, 3 plaid aqua bags, 2 clear black bags.
line_exp = re.compile(r'(?P<outer>\w+ \w+) bags contain (?P<inner>((\d+) (\w+ \w+) bags?[,.] ?)+)')
colors_exp = re.compile(r'((\d+) (\w+ \w+) bags?[,.] ?)')
for l in srules:
    if 'no other bags' in l or not l:
        continue
    match = re.match(line_exp, l)
    #print(match['outer'], '!', match['inner'])
    inner = [c for (_, n, c) in re.findall(colors_exp, match['inner'])]
    print(inner)
    for c in inner:
        rules[c].append(match['outer'])

good = set()
def rec(c):
    good.add(c)
    for d in rules[c]:
        rec(d)
rec('shiny gold')
print(good)
print(len(good) - 1) # shiny gold itself
