"""
to find the best strat for a blueprint
we can define a strat as a sequence of target robots
f.e.
[clay, obsidian, geode]
will not build anything till it has enough materials
    for a clay robot,
then it will not build anything till it has enough
    for an obsidian robot,
then it will not build anything till it has enough
    for a geode robot.

each robot collects 1 per minute
24 minutes total
"""
import math

ore = 'ore' # ore
clay = 'clay' # clay
obs = 'obsidian' # obsidian
geo = 'geode' # geode

materials = (ore,clay,obs,geo)

#bp = {
#    ore: {ore:4},
#    clay: {ore:2},
#    obs: {ore:3, clay:14},
#    geo: {ore:2, obs:7},
#}
#
#for k in bp:
#    for m in materials:
#        bp[k].setdefault(m, 0)

class ImpossibleException(Exception):
    pass

def time_needed(bp, target, robots, items, verbose=False):
    max_t = 0
    for m, n in bp[target].items():
        if n == 0:
            continue
        if robots[m] == 0:
            #print(robots, robots[m], m)
            raise ImpossibleException()
        if verbose:
            print("we need",n,m,"of which we have",items[m],"and make",
                  robots[m],"per minute")
            print("so we need to make", (n - items[m]))
        t = math.ceil((n - items[m])/robots[m])
        max_t = max(max_t, t)
    return max_t+1

def display_strat(bp, path, time=32, debug=False):
    _print = lambda *args, **kwargs: None
    if debug:
        _print = print
    robots = {ore: 1, clay: 0, obs: 0, geo: 0}
    items = {ore: 0, clay: 0, obs: 0, geo: 0}
    tt = 1
    nextp = path.pop(0)
    nextt = time_needed(bp, nextp, robots, items)
    _print(nextt)
    log = []
    for turn in range(time):
        _print("turn", turn+1, end=" ")
        t, p = nextt, nextp
        make = None
        if tt == t:
            tt = 1
            items = {k: (v - bp[p][k]) for k,v in items.items()}
            make = p
            log.append(p)
        else:
            log.append([])
            _print('idle!', [(k, v) for k,v in items.items() if v])
            tt += 1
            missing_materials = {}
            spare_materials = {}
            if p is not None:
                # what do we need to make the next thing?
                for material, needed in bp[p].items():
                    if items[material] < needed:
                        missing_materials[material] = needed-items[material]
                        _print("\tneed", needed-items[material], material)
                    else:
                        x = items[material]+robots[material]-needed
                        if x > 0:
                            spare_materials[material] = x
            could_make = []
            for product in materials:
                for material, needed in bp[product].items():
                    if not needed:
                        continue
                    if (material not in spare_materials or
                            spare_materials[material] < needed or
                            items[material] < needed):
                        break
                else:
                    could_make.append(product)
            if could_make:
                _print("\tcould be making", could_make)
                _print("\tspare materials", spare_materials)
            else:
                _print("\tspare materials", spare_materials)
            log[-1] = (tuple(missing_materials.keys()), tuple(could_make))
        #print("collecting... items before:", items)
        items = {k: (v + robots[k]) for k,v in items.items()}
        #print("collecting... items after: ", items)
        #print(items)
        if make:
            _print("made a", p, 'bot', '!!' if p == geo else '')
            robots[p] += 1
            nextp, nextt = None, None
            if path:
                nextp = path.pop(0)
                nextt = time_needed(bp, nextp, robots, items)
    _print("leftover", nextp)
    _print("total", items[geo])
    return items[geo], log, nextp

# example 1
bp = {ore: {ore: 4, clay: 0, obs: 0, geo: 0},
 clay: {ore: 2, clay: 0, obs: 0, geo: 0},
 obs: {ore: 3, clay: 14, obs: 0, geo: 0},
 geo: {ore: 2, obs: 7, clay: 0, geo: 0}}

# example 2
bp = {ore: {ore: 2, clay: 0, obs: 0, geo: 0},
 clay: {ore: 3, clay: 0, obs: 0, geo: 0},
 obs: {ore: 3, clay: 8, obs: 0, geo: 0},
 geo: {ore: 3, obs: 12, clay: 0, geo: 0}}

# input 1
bp = {'id': 0, 'ore': {'ore': 2, 'clay': 0, 'obsidian': 0, 'geode': 0}, 'clay': {'ore': 4, 'clay': 0, 'obsidian': 0, 'geode': 0}, 'obsidian': {'ore': 4, 'clay': 20, 'obsidian': 0, 'geode': 0}, 'geode': {'ore': 3, 'obsidian': 14, 'clay': 0, 'geode': 0}}

# input 2
bp = {'id': 0, 'ore': {'ore': 3, 'clay': 0, 'obsidian': 0, 'geode': 0}, 'clay': {'ore': 3, 'clay': 0, 'obsidian': 0, 'geode': 0}, 'obsidian': {'ore': 2, 'clay': 20, 'obsidian': 0, 'geode': 0}, 'geode': {'ore': 2, 'obsidian': 20, 'clay': 0, 'geode': 0}}

# ore ore ore clay clay clay clay clay clay clay obs clay obs clay clay obs clay obs geo obs obs geo obs geo geo
#bp = {'ore': {'ore': 2, 'clay': 0, 'obs': 0, 'geo': 0},
# 'clay': {'ore': 4, 'clay': 0, 'obs': 0, 'geo': 0},
# 'obs': {'ore': 4, 'clay': 20, 'obs': 0, 'geo': 0},
# 'geo': {'ore': 3, 'obs': 14, 'clay': 0, 'geo': 0}}

import sys
if sys.argv[1:]:
    display_strat(bp, sys.argv[1:])
    quit()

def optimize(path, debug=False):
    best_score = 0
    best_score, log, leftover = display_strat(bp, list(path), debug=debug)
    tried = set()
    for i in range(50):
        modlog = list(log)
        for n, x in enumerate(log):
            attempt_ready = False
            if type(x) is tuple:
                missing_materials, could_make = x
                for p in missing_materials:
                    if p in could_make:
                        if (n, p, tuple(log)) not in tried:
                            if debug:
                                print('filling idleness at', n, 'with', p)
                            modlog[n] = p
                            attempt_ready = True
                            break
            if attempt_ready:
                break
        else:
            if debug:
                print("nothing I tried worked")
            return best_score, path
            #break
        new_path = [x for x in modlog if type(x) is not tuple]
        #print("new path", new_path)
        score, newlog, leftover = display_strat(bp, list(path), debug=debug)
        if score >= best_score:
            if debug:
                print("yay", score)
            best_score = score
            path = new_path+[geo, geo, geo]
            log = newlog
        else:
            if debug:
                print("didn't do much", score, best_score)
    return best_score, path

print('BP:')
for m in materials:
    print(m, [(k,v) for k,v in bp[m].items() if v>0])
print()

#print(display_strat(bp, [ore]*2 +
#                    [clay]*7 +
#                    [obs]*1 + # 15
#                    [clay]*2 +
#                    [obs] + # 18
#                    [clay]*2 +
#                    [obs]*2 + # 21 22
#                    [clay]*1 + # 23
#                    [obs]*1 + # 24
#                    [geo]*1 + # 25
#                    [obs]*2 + # 26
#                    [geo]*10 #
#                    , debug=True))

"""
per fer 1 geode bot necessito 20 obs
per fer 1 obs bot necessito 20 clay
"""

print(display_strat(bp, [ore]*2 +
                    [clay] * 8 + # 8
                    [obs] + # 16
                    [clay] + # 17
                    [obs] +
                    [clay] + # 19
                    [obs] +
                    [clay] + # 21
                    [obs] +
                    [obs] +
                    [geo] + # 26
                    [geo] + # 26
                    [obs] +
                    [geo] * 10,
                    debug=True))

#print(optimize(['ore', 'ore', 'ore', 'clay', 'obsidian', 'geode', 'geode', 'geode', 'geode', 'geode', 'geode', 'geode', 'geode', 'geode', 'geode'], debug=True))

print()
print('BP:')
for m in materials:
    print(m, [(k,v) for k,v in bp[m].items() if v>0])

#best_score = 0
#best = None
#for o in range(10):
#    for c in range(1, 10):
#        path = [ore]*o + [clay]*c + [obs] + [geo]*10
#        score, opath = optimize(path)
#        if score > best_score:
#            best_score = score
#            best = path
#print(best_score, path)
