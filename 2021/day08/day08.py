def get_input(fn="input.txt"):
    with open(fn) as f:
        s = f.read().strip().split('\n')
    return s

def part1():
    lines = get_input()
    good = 0
    for line in lines:
        inp, out = line.split(" | ")
        lens = [len(d) for d in out.split()]
        good += sum(1 for x in lens if x in
                      (2, 4, 3, 7))
    print(good)

from itertools import permutations
def guess_mapping(inp):
    possible_mappings = list(permutations('abcdefg'))
    #print(type(possible_mappings))
    words = [frozenset(word) for word in inp.split()]
    #print(words)
    for mapping in possible_mappings:
        a, b, c, d, e, f, g = mapping
        # test if 1 is possible:
        if frozenset((c, f)) not in words:
            continue
        # test if 4 is possible:
        if frozenset((b, c, d, f)) not in words:
            continue
        # test if 7 is possible:
        if frozenset((a, c, f)) not in words:
            continue
        # test if 0 is possible:
        if frozenset((a, b, c, e, f, g)) not in words:
            continue
        # test if 2 is possible:
        if frozenset((a, c, d, e, g)) not in words:
            continue
        # test if 3 is possible:
        if frozenset((a, c, d, f, g)) not in words:
            continue
        # test if 5 is possible:
        if frozenset((a, b, d, f, g)) not in words:
            continue
        # test if 6 is possible:
        if frozenset((a, b, d, e, f, g)) not in words:
            continue
        # test if 9 is possible:
        if frozenset((a, b, c, d, f, g)) not in words:
            continue
        return mapping

def part2():
    lines = get_input("input.txt")
    sol = 0
    for line in lines:
        inp, out = line.split(" | ")
        mapping = guess_mapping(inp)
        print(mapping)
        a, b, c, d, e, f, g = mapping
        mapping = {a: "a", b: "b", c: "c", d: "d",
                   e: "e", f: "f", g: "g"}
        nums = {
            "abcefg": 0,
            "cf": 1,
            "acdeg": 2,
            "acdfg": 3,
            "bcdf": 4,
            "abdfg": 5,
            "abdefg": 6,
            "acf": 7,
            "abcdefg": 8,
            "abcdfg": 9,
        }

        mapped = ["".join(sorted([mapping[c] for c in word])) for word in out.split()]
        nummed = int(''.join([str(nums[word]) for word in mapped]))
        print(nummed)
        sol += nummed
    print(sol)

if __name__ == "__main__":
    part1()
    part2()
