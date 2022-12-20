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
            #print('trying to make', target, 'but no', m)
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
            _print('idle!', items)
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
                        spare_materials[material] = items[material]+robots[material]-needed
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
#bp = {'ore': {'ore': 4, 'clay': 0, 'obs': 0, 'geo': 0},
# 'clay': {'ore': 2, 'clay': 0, 'obs': 0, 'geo': 0},
# 'obs': {'ore': 3, 'clay': 14, 'obs': 0, 'geo': 0},
# 'geo': {'ore': 2, 'obs': 7, 'clay': 0, 'geo': 0}}
#
## example 2
#bp = {'ore': {'ore': 2, 'clay': 0, 'obs': 0, 'geo': 0},
# 'clay': {'ore': 3, 'clay': 0, 'obs': 0, 'geo': 0},
# 'obs': {'ore': 3, 'clay': 8, 'obs': 0, 'geo': 0},
# 'geo': {'ore': 3, 'obs': 12, 'clay': 0, 'geo': 0}}


# ore ore ore clay clay clay clay clay clay clay obs clay obs clay clay obs clay obs geo obs obs geo obs geo geo
#bp = {'ore': {'ore': 2, 'clay': 0, 'obs': 0, 'geo': 0},
# 'clay': {'ore': 4, 'clay': 0, 'obs': 0, 'geo': 0},
# 'obs': {'ore': 4, 'clay': 20, 'obs': 0, 'geo': 0},
# 'geo': {'ore': 3, 'obs': 14, 'clay': 0, 'geo': 0}}

import sys
if sys.argv[1:]:
    display_strat(bp, sys.argv[1:])
    quit()

def optimize(bp, path, debug=False):
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
        try:
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
        except ImpossibleException:
            if debug:
                print("didn't even complete")
    return best_score, path

def superoptimize(bp):
    #print(optimize([ore] + [clay]*7 + [obs]*4 + [geo]*10, debug=True))
    best_score = 0
    best = None
    for z in [[], [clay], [ore, clay], [ore, ore, clay], [clay, clay]]:
        for o in range(25):
            for c in range(1, 25):
                path = z + [ore]*o + [clay]*c + [obs] + [geo]*10
                #print('trying with ore', o, 'clay', c)
                score, opath = optimize(bp, path)
                if score > best_score:
                    best_score = score
                    best = opath
    return best_score, best

import sys
qualities = []
for n, line in enumerate(sys.stdin):
    if n == 3:
        break
    if not line:
        continue
    print(line)
    # Blueprint 1: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 20 clay. Each geode robot costs 3 ore and 14 obsidian.
    bp = {"id": n}
    for sub in line.split('Each')[1:]:
        sub = sub.strip()
        name = sub.split(' ')[0]
        costs = sub.split('costs')[1].strip().strip('.')
        costs = [c.split() for c in costs.split(' and ')]
        bp[name] = {k: int(v) for v,k in costs}
        for m in materials:
            bp[name].setdefault(m, 0)

    print('BP:')
    for m in materials:
        print(m, [(k,v) for k,v in bp[m].items() if v>0])
    print()

    points, path = superoptimize(bp)
    if points:
        print(bp)
        print(n+1, points)
        print(path)
        display_strat(bp, path, debug=True)
        print()
    qualities.append(points)

print(qualities[0]*qualities[1]*qualities[2])
