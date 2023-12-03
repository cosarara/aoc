from collections import defaultdict
import re
with open("input.txt") as f:
    content = f.read()

grid = content.strip("\n").split("\n")
def get(x, y):
    if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
        return '.'
    return grid[y][x]

def print_region_marked(x, y, marked):
    print(marked)
    for y0 in range(y-5, y+5):
        for x0 in range(x-10, x+15):
            c = get(x0, y0)
            if (x0, y0) in marked:
                print(f"\033[4m{c}\033[0m", end='')
            else:
                print(c, end='')
        print('')
    print('')

def check_around(line_n, n, length):
    marked = set()
    for y in (line_n-1, line_n, line_n+1):
        for x in range(n-1, n+length+1):
            marked.add((x, y))
            if c := get(x, y) == "*":
                #print_region_marked(n, line_n, set())
                print_region_marked(n, line_n, marked)
                return x, y

    print_region_marked(n, line_n, marked)
    return False

around_star = defaultdict(list)
for y, line in enumerate(grid):
    for x, c in enumerate(line):
        part = line[x:]
        if get(x-1, y) in "0123456789":
            continue
        if m := re.match(r"\d+", part):
            num = m[0]
            if coords := check_around(y, x, len(num)):
                around_star[coords].append(int(num))

total = 0
for gear, nums in around_star.items():
    #print(gear, nums)
    if len(nums) == 2:
        a, b = nums
        total += a*b

print(total)
