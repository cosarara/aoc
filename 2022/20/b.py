import sys

result = lambda n: (n[(n.index(0)+1000)%(len(n))] +
                    n[(n.index(0)+2000)%(len(n))] +
                    n[(n.index(0)+3000)%(len(n))])
result2 = lambda m0: (look_right(m0, 1000)['v']+
                      look_right(m0, 2000)['v']+
                      look_right(m0, 3000)['v'])

def strictindex(l, v):
    for i, u in enumerate(l):
        if v is u:
            return i
    raise ValueError(f"{v} is not in list")

VERBOSE = '-v' in sys.argv
def mix(l, verbose=VERBOSE):
    original_list = [[i] for i in l]
    newl = list(original_list)
    newls = []
    for i in range(10):
        for i, v in enumerate(original_list):
            #pos = newl.index(v)
            pos = strictindex(newl, v)
            if verbose:
                print(newl, pos, i, v)
            newl.pop(pos)
            newpos = (pos+v[0])%(len(l)-1)
            #newpos = (pos+i-1)%(len(newl))
            if verbose:
                #print(f'moving {v} between {newl[newpos]} {newl[(newpos+1)%len(newl)]} {newpos}')
                print('pos, newpos', pos, newpos)
            newl.insert(newpos, v)
            #newl.insert((newpos+1)%len(newl), v)
            newls.append(to_0list([x for (x,) in newl]))
    if verbose:
        print(newl)
    return [x for (x,) in newl]

def circle(l):
    nodes = [{'v': l[0], 'next': None, 'prev': None}]
    node_map = {0: nodes[0]}
    for i, v in enumerate(l[1:]):
        prev = nodes[-1]
        n = {'v': v, "prev": prev, "next": None}
        prev['next'] = n
        nodes.append(n)
        node_map[i+1] = n
    nodes[0]['prev'] = nodes[-1]
    nodes[-1]['next'] = nodes[0]
    return node_map

def look_left(node, i):
    tmp = node
    for i in range(i):
        tmp = tmp['prev']
    return tmp

def look_right(node, i):
    tmp = node
    for i in range(i):
        tmp = tmp['next']
    return tmp

def print_circle(node_map):
    tmp = node_map[0]
    for _ in range(len(node_map)+1):
        print(tmp['v'], end=' ')
        tmp = tmp['next']
    print()

def circle_to_0list(node_map):
    l = []
    tmp = node_map[0]
    for _ in range(len(node_map)):
        l.append(tmp['v'])
        tmp = tmp['next']
    return to_0list(l)

def to_0list(l):
    i = l.index(0)
    return l[i:]+l[:i]

def mix3(l, verbose=VERBOSE):
    newls = []
    #newl = list(l)
    original_list = [[i] for i in l]
    newl = list(original_list)

    for v in original_list:
        if verbose:
            print(newl, v)
        if v[0] == 0:
            #newls.append(to_0list(newl))
            newls.append(to_0list([x for (x,) in newl]))
            continue
        #pos = newl.index(i)
        pos = strictindex(newl, v)
        if v[0] >= 0:
            for j in range(v[0]):
                # swap node with the element on the right
                other = (pos+1) % len(l)
                newl[pos], newl[other] = newl[other], newl[pos]
                pos = other
        else:
            for j in range(-v[0]):
                # swap node with element on the left
                other = (pos-1) % len(l)
                newl[pos], newl[other] = newl[other], newl[pos]
                pos = other
        #newls.append(to_0list(newl))
        newls.append(to_0list([x for (x,) in newl]))
    if verbose:
        print(newl)
    return [x for (x,) in newl]

def mix4(l, verbose=VERBOSE):
    newls = []
    node_map = circle(l)
    for i, v in enumerate(l):
        if verbose:
            # print
            print_circle(node_map)
            # end print
            print('moving', v)
        n = node_map[i]
        old_prev = n['prev']
        old_next = n['next']
        if v == 0:
            newls.append(circle_to_0list(node_map))
            continue
        # close the gap
        old_prev['next'] = old_next
        old_next['prev'] = old_prev
        if v >= 0:
            # will go after the found element
            target_left = look_right(n, v)
            target_right = target_left['next']
        else:
            # will go before the found element
            target_right = look_left(n, -v)
            target_left = target_right['prev']
        #if old_prev == target_left:
            # we didn't move
            #print("didn't move", i, target_right['v'], target_left['v'])
            #continue
        #print('between', target_left['v'], 'and', target_right['v'])
        # move to target
        target_left['next'] = n
        target_right['prev'] = n
        n['prev'] = target_left
        n['next'] = target_right
        newls.append(circle_to_0list(node_map))
    if verbose:
        print_circle(node_map)
    return node_map

#for i in range(1000):
#    l = list(randinput())
#    if not 0 in l:
#        l += [0]
#        random.shuffle(l)
#    print(l)
#    out1 = to_0list(mix(l))
#    out3 = to_0list(mix3(l))
#    out4 = circle_to_0list(mix4(l))
#    print('outs', out1[:10], out3[:10], out4[:10])
#    if out1 != out3:
#        print("1 and 3 differ")
#        print(out1, out3)
#        break
#    if out1 != out4:
#        print("1 and 4 differ")
#        print(out1, out3)
#        break
#    if out3 != out4:
#        print("3 and 4 differ")
#        print(out1, out3)
#        break

example = """1
2
-3
3
-2
0
4"""

inp = sys.stdin.read()

l = [int(a) for a in inp.split()]

print('approach #1 - find new position by index and math')
m = [811589153 * a for a in l]
m = mix(m)
print(result(m))

#print('approach #3 - swapping')
#m = mix3(l)
#print(result(m))
#
#print('approach #4 - circle list, closing gap at the start')
#m = mix4(l)
#print(result2(m[l.index(0)]))
