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
obs = 'obs' # obsidian
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

def display_strat(bp, path, time=32):
    robots = {ore: 1, clay: 0, obs: 0, geo: 0}
    items = {ore: 0, clay: 0, obs: 0, geo: 0}
    tt = 1
    nextp = path.pop(0)
    nextt = time_needed(bp, nextp, robots, items)
    print(nextt)
    for turn in range(time):
        print("turn", turn, end=" ")
        t, p = nextt, nextp
        #t, p = None, None
        #if path:
        #    t, p = path[0]
        make = None
        if tt == t:
            #t, p = path.pop(0)
            tt = 1
            #print("making a", p, 'bot', tuple((v, k) for k,v in
            #                                  bp[p].items()
            #                                  if v))
            items = {k: (v - bp[p][k]) for k,v in items.items()}
            make = p
        else:
            print('idle!', items)
            tt += 1
        #print("collecting... items before:", items)
        items = {k: (v + robots[k]) for k,v in items.items()}
        #print("collecting... items after: ", items)
        #print(items)
        if make:
            print("made a", p, 'bot')
            robots[p] += 1
            nextp, nextt = None, None
            if path:
                nextp = path.pop(0)
                nextt = time_needed(bp, nextp, robots, items)
    print("leftover", path)


def hashable(bpid, robots, items, turns):
    return (bpid,
            *tuple(robots[m] for m in materials),
            *tuple(items[m] for m in materials),
            turns)

def make_memoized_best_strat():
    lookup = {}
    def f(bp, robots, items, turns, path):
        h = hashable(bp[id], robots, items, turns)
        try:
            v = lookup[h]
        except KeyError:
            v = best_strat(bp, robots, items, turns, path)
            lookup[h] = v
        return v
    return f

def best_strat(bp, robots, items, turns, path):
    best_path = []
    best_geodes = 0
    if not turns:
        return items[geo], path

    possible_paths = []
    for p in reversed(materials):
        try:
            t = time_needed(bp, p, robots, items)
        except ImpossibleException:
            #print('impossible to make a', p, 'robot')
            continue
        #print('takes', t, 'to make a', p, 'robot')
        if t <= turns-1: # because making anything on turn 24 is stupid
            if t == turns-2 and p != geo:
                continue # would be stupid too
            possible_paths.append((p, t))

    if not possible_paths:
        # just wait till the end of the game
        tgeo = items[geo] + robots[geo] * turns
        return tgeo, path

    for p, t in possible_paths:
                        # items + produced - taken
        new_items = {k: (v + robots[k]*t - bp[p][k])
                     for k,v in items.items()}
        new_robots = dict(robots)
        new_robots[p] += 1
        tgeo, ppath = m_best_strat(bp, new_robots, new_items,
                                turns-t, path+[(t, p)])
        if tgeo > best_geodes:
            best_geodes = tgeo
            best_path = ppath

    #if turns == 18 and best_path:
    #    print(best_geodes, best_path)
    return best_geodes, best_path

m_best_strat = make_memoized_best_strat()
#m_best_strat = best_strat

#print('example', (clay, clay, clay, obs, clay, obs, geo, geo))
#points, best = best_strat(bp, {ore: 1, clay: 0, obs: 0, geo: 0},
#                 {ore: 0, clay: 0, obs: 0, geo: 0}, 24, [])
#print(points, best)
#
#display_strat(bp, best)

import sys
qualities = []
for n, line in enumerate(sys.stdin):
    if n == 3:
        break
    if not line:
        continue
    # Blueprint 1: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 20 clay. Each geode robot costs 3 ore and 14 obsidian.
    bp = {id: n}
    for sub in line.split('Each')[1:]:
        sub = sub.strip().replace('obsidian', 'obs')
        name = sub.split(' ')[0]
        costs = sub.split('costs')[1].strip().strip('.')
        costs = [c.split() for c in costs.split(' and ')]
        bp[name] = {k: int(v) for v,k in costs}
        for m in materials:
            bp[name].setdefault(m, 0)
    points, best = best_strat(bp, {ore: 1, clay: 0, obs: 0, geo: 0},
                              {ore: 0, clay: 0, obs: 0, geo: 0}, 32, [])
    if points:
        print(bp)
        print(n+1, points, best)
    qualities.append(points)

print(quality[0]*quality[1]*quality[2])
