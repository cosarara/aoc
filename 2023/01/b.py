import re

pattern = re.compile(r"[0-9]|one|two|three|four|five|six|seven|eight|nine")

def numeric(s):
    l = ("one",
         "two",
         "three",
         "four",
         "five",
         "six",
         "seven",
         "eight",
         "nine")
    if s in l:
        return str(l.index(s) + 1)
    return s

def findstart(line):
    for i, _ in enumerate(line):
        substart = line[i:]
        if m := re.match(pattern, substart):
            return m[0]

def findend(line):
    for i, _ in enumerate(line):
        subend = line[-1-i:]
        if m := re.match(pattern, subend):
            return m[0]

specials = [0, 0]
with open("input.txt") as f:
    total = 0
    for line in f:
        matches = re.findall(pattern, line)
        start = numeric(matches[0])
        end = numeric(matches[-1])
        start2 = numeric(findstart(line))
        end2 = numeric(findend(line))
        val1 = int(start + end)
        val2 = int(start2 + end2)

        if val1 != val2:
            print(val1, val2, line[:-1])
            specials[0] += int(start + end)
            specials[1] += int(start2 + end2)
        val = int(start + end)
        total += val

#print(total)
print(specials)
