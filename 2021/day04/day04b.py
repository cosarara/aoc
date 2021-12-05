from collections import defaultdict

with open("input.txt") as f:
    s = f.read().split('\n\n')

nums = [int(n) for n in s[0].split(',')]
boards = [
    [[int(m) for m in n.strip().split()]
     for n in x.strip().split('\n')]
    for x in s[1:]]
print(nums)
print(boards[0])

def allwon(won, boards):
    for n, _ in enumerate(boards):
        if not won[n]:
            return False
    return True

def play():
    hit = defaultdict(lambda: False)
    won = defaultdict(lambda: False)
    for num in nums:
        for boardn, board in enumerate(boards):
            if won[boardn]:
                continue
            for y, row in enumerate(board):
                for x, n in enumerate(row):
                    if n == num:
                        hit[(boardn, x, y)] = True
                        # check h
                        found = True
                        for xx in range(5):
                            if not hit[(boardn, xx, y)]:
                                found = False
                                break
                        if found:
                            print('found h', boardn, x, y, n)
                            won[boardn] = True
                            if allwon(won, boards):
                                return boardn, hit, num
                            break
                        # check v
                        found = True
                        for yy in range(5):
                            if not hit[(boardn, x, yy)]:
                                found = False
                                break
                        if found:
                            print('found v', boardn, x, y, n)
                            won[boardn] = True
                            if allwon(won, boards):
                                return boardn, hit, num
                            break
                if won[boardn]:
                    break
boardn, hit, num = play()
score = sum([num for y, row in enumerate(boards[boardn])
             for x, num in enumerate(row) if not hit[(boardn, x, y)]])
print(num, score)
print(num*score)
