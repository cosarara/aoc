import functools

@functools.cache
def fit(line, groups):
    line = line.lstrip(".")
    while True:
        if len(line) < len(groups) - 1 + sum(groups):
            return 0
        group = groups[0]
        if not line or len(line) < group:
            #print("not enough input")
            return 0

        #print("fitting", line, groups)
        c = line[0]
        if c == "?":
            return (fit(line[1:], groups)+fit("#"+line[1:], groups))
        if c == "#":
            if "." in line[:group]:
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
            line = line[group+1:].lstrip(".")
            groups = groups[1:]
            if not groups:
                if not "#" in line:
                    #print("finished ok")
                    return 1
                #print("there was more input but no groups")
                return 0

def arrangements(line):
    condition, groups = line.split(" ")
    groups = tuple([int(s) for s in groups.split(',')] * 5)
    condition = "?".join([condition]*5)
    print(condition, groups)
    return fit(condition, groups)

#condition = '?###??????????###??????????###??????????###??????????###????????'
#groups = [3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1]
#condition = '?.#??????.#????#????.#??????.#????#????.#??????.#????#????.#??????.#????#????.#??????.#????#??'
#groups = [1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1, 7]
#condition = '??.???#???????.???#???????.???#???????.???#???????.???#????'
#groups = tuple([1, 4, 1, 1, 4, 1, 1, 4, 1, 1, 4, 1, 1, 4, 1])
#fit(condition, groups)

total = 0
import sys
with open(sys.argv[1]) as f:
    for line in f:
        n = arrangements(line.strip())
        print(n)
        total += n

print(total)
