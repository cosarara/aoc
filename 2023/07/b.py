from collections import Counter

with open("input.txt") as f:
    lines = f.read().strip().split("\n")

total = 0

def value(line):
    hand, bid = line
    _, best_card = max(
        [(v, k) for k, v in Counter(hand).items() if k != 'J'] or [(1, 'J')])
    counter = Counter(hand.replace("J", best_card))
    hand = (hand.replace("A", "e")
                .replace("K", "d")
                .replace("Q", "c")
                .replace("J", "0") # weaker than even 2
                .replace("T", "b"))
    return (sorted(counter.values(), reverse=True), hand)

lines = [line.split() for line in lines]
lines = [(hand, int(bid)) for hand, bid in lines]

print(lines)

print([(line, value(line)) for line in lines])
print(sorted(lines, key=value))
print(sum([(i+1) * v for (i, (h, v)) in enumerate(sorted(lines, key=value))]))
