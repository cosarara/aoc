def get_input(fn="input.txt"):
    with open(fn) as f:
        s = f.read().strip().split(',')
    return [int(x) for x in s]

def part1():
    state = get_input()
    for _ in range(80):
        new_state = []
        for fish in state:
            if fish == 0:
                new_state.append(6)
                new_state.append(8)
            else:
                new_state.append(fish-1)
        state = new_state

    print(len(state))

def zero_fish_naive(days, verbose=False):
    state = [0]
    for _ in range(days):
        if verbose:
            print(state)
        new_state = []
        for fish in state:
            if fish == 0:
                new_state.append(6)
                new_state.append(8)
            else:
                new_state.append(fish-1)
        state = new_state
    return len(state)

def any_fish(f, n, days):
    return f(days-n)

def n_fish(f, initial, days):
    return sum([any_fish(f, n, days)
                for n in initial])

import functools

@functools.cache
def zero_fish_rec(days, verbose=False):
    if days < 0:
        return 1
    if days == 0:
        return 1
    return (zero_fish_rec(days-7) +
            zero_fish_rec(days-9))

def zero_fish_iter(days, verbose=False):
    """ the iterative solution here should be optimal;
    it could be made faster by rolling around a fixed-size
    array properly initialized to 1s and rolling around
    only the indices."""
    if days == 0:
        return 1
    window = []
    for i in range(days):
        # 7 takes -2st and 0th = 2
        # 8 takes -1st and 1st = 3
        # 9 takes 0th and 2nd = 3
        # 10 takes 1st and 3rd = 4
        i = len(window) - 9
        j = len(window) - 7
        if i < 0:
            a = 1
        else:
            a = window[i]
        if j < 0:
            b = 1
        else:
            b = window[j]
        window.append(a+b)
        #if len(window) > 9: # popping makes it slow actually
        #    window.pop(0)
    return window[-1]

def part2():
    state = get_input()
    #print(n_fish(zero_fish_rec, state, 256))
    print(n_fish(zero_fish_iter, state, 256))

if __name__ == "__main__":
    part1()
    part2()
