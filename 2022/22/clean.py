import sys
import re

lines = list(sys.stdin.read().strip('\n').split('\n'))
with open('example') as exf:
    lines_example = list(exf.read().strip('\n').split('\n'))

def make_map_path(text):
    map = lines[:-2]
    path = re.findall(r'\d+|\D', lines[-1])
    return map, path
map, path = make_map_path(lines)
mape, pathe = make_map_path(lines_example)

print('map')
print("\n".join(map))
print('path', path)

def move(pos, facing, map):
    x, y = pos
    wrapped = False
    if facing == '>':
        x += 1
        if x>=len(map[y]):
            for xx, c in enumerate(map[y]):
                x = xx
                if c != ' ':
                    break
            wrapped = True
        return (x, y), wrapped
    elif facing == '<':
        x -= 1
        if x==-1 or map[y][x] == ' ':
            x = len(map[y])-1
            wrapped = True
        return (x, y), wrapped
    elif facing == '^':
        y -= 1
        if y==-1 or x >= len(map[y]) or map[y][x] == ' ':
            y += 1
            while y<len(map)-1 and x < len(map[y]) and map[y][x] != ' ':
                y += 1
            y -= 1
            wrapped = True
        return (x, y), wrapped
    elif facing == 'v':
        y += 1
        if y==len(map) or x >= len(map[y]) or map[y][x] == ' ':
            y -= 1
            while y>0 and x < len(map[y]) and map[y][x] != ' ':
                y -= 1
            y += 1
            wrapped = True
        return (x, y), wrapped

print('testing')
print(move((10, 6), '>', mape), 'nowrap 11 6')
print(move((11, 6), '>', mape), 'wrap 0 6')
print(move((1, 6), '<', mape), 'nowrap 0 6')
print(move((0, 6), '<', mape), 'wrap 11 6')
print(move((0, 5), '^', mape), 'nowrap 0 4')
print(move((0, 4), '^', mape), 'wrap 0 7')
print(move((9, 1), '^', mape), 'nowrap 9 0')
print(move((0, 6), 'v', mape), 'nowrap 0 7')
print(move((0, 7), 'v', mape), 'wrap 0 4')

def run(map, path):
    start = None
    for y, l in enumerate(map):
        for x, c in enumerate(l):
            if map[y][x] == '.':
                start = (x, y)
                break
        if start:
            break
    facing = '>'
    pos = start
    print('start', start)
    history = {start: (facing, 100)}
    for naction, action in enumerate(path):
        print(action)
        if action.isnumeric():
            steps = int(action)
            for step in range(steps):
                next_pos, wrapped = move(pos, facing, map)
                nx, ny = next_pos
                if map[ny][nx] == ' ':
                    raise Exception('bugged', x, y,
                                    facing, nx, ny,
                                    map[nx][ny])
                if map[ny][nx] == '.':
                    pos = next_pos
                    print('moved to', pos)
                else:
                    print('hit a wall')
                    break
                history[pos] = (facing, 100)
        elif action == 'R':
            facing = {'^':'>', '>':'v', 'v':'<', '<':'^'}[facing]
            print('R, now', facing)
        elif action == 'L':
            facing = {'^':'<', '<':'v', 'v':'>', '>':'^'}[facing]
            print('L, now', facing)
        else:
            raise Exception('ur a dumdum')
        history[pos] = (facing, 100)
        for hpos in history:
            hfacing, age = history[hpos]
            history[hpos] = (hfacing, max(0, age-5))
            x, y = pos
            if map[y][x] != '.':
                raise Exception('wtf')

    finalpos, finalfacing = pos, facing
    print(finalpos, finalfacing)
    facev = {'>': 0, 'v': 1, '<':2, '^':3}[finalfacing]
    print(facev)
    print((finalpos[1]+1)*1000 + (finalpos[0]+1)*4 + facev)
    return history, pos, facing

h, finalpos, finalfacing = run(map, path)
for y, l in enumerate(map):
    for x, c in enumerate(l):
        if (x, y) in h:
            print(h[(x,y)], end='')
        else:
            print(c, end='')
    print()

print(finalpos, finalfacing)
facev = {'>': 0, 'v': 1, '<':2, '^':3}[finalfacing]
print(facev)
print((finalpos[1]+1)*1000 + (finalpos[0]+1)*4 + facev)
