import sys

def fit(line, groups):
    #print("fitting", line, groups)
    if not groups:
        if not "#" in line:
            #print("finished ok")
            return 1
        #print("there was more input but no groups")
        return 0
    group = groups[0]
    if not line or len(line) < group:
        #print("not enough input")
        return 0
    c = line[0]
    if c == "#":
        for cc in line[:group]:
            if cc == ".":
                #print("too short")
                return 0
        if len(line) == group: # perfect match, end
            if len(groups) == 1: # this was the last group
                #print("finished ok 2")
                return 1
            #print("line done but more groups")
            return 0 # there were other groups
        if line[group] == "#": # too long
            #print("too long")
            return 0
        return fit(line[group+1:], groups[1:])
    if c == ".":
        return fit(line[1:], groups)
    if c == "?":
        return (fit("."+line[1:], groups)+fit("#"+line[1:], groups))

def arrangements(line):
    condition, groups = line.split(" ")
    groups = [int(s) for s in groups.split(',')]
    print(condition, groups)
    return fit(condition, groups)

total = 0
with open(sys.argv[1]) as f:
    for line in f:
        n = arrangements(line.strip())
        print(n)
        total += n

print(total)
