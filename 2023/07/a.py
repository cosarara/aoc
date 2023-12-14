from collections import Counter

with open("input.txt") as f:
    lines = f.read().strip().split("\n")

total = 0

def value(line):
    hand, bid = line
    hand = (hand.replace("A", "e")
                .replace("K", "d")
                .replace("Q", "c")
                .replace("J", "b")
                .replace("T", "a"))
    counter = Counter(hand)
    return (sorted(counter.values(), reverse=True), hand)

lines = [line.split() for line in lines]
lines = [(hand, int(bid)) for hand, bid in lines]

print(lines)

print([(line, value(line)) for line in lines])
print(sorted(lines, key=value))
print(sum([(i+1) * v for (i, (h, v)) in enumerate(sorted(lines, key=value))]))
