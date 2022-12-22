import sys
import re
import pygame as pg

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

pg.init()
radius = 100
screen = pg.display.set_mode((800, 1040))
font = pg.font.SysFont(None, 24)
clock = pg.time.Clock()
scale = 5
def px(x, y, color=(255,255,255), age=100):
    if age != 100:
        color = [min(255, c+(255-age*2.55)) for c in color]
    screen.set_at((x+25, y+25), color)

def draw_bright(x, y, age):
    color = [min(255, (150+age*1.05)) for _ in range(3)]
    screen.fill(color, pg.Rect(x*scale+25, y*scale+25,
                                       scale-1, scale-1))

def draw_space(x, y):
    screen.fill((150,150,150), pg.Rect(x*scale+25, y*scale+25,
                                       scale-1, scale-1))
    #for yy in range(3):
    #    for xx in range(3):
    #        px(xx+scale*x, yy+scale*y, (255,255,255))

def draw_wall(x, y):
    screen.fill((0,0,0), pg.Rect(x*scale+25, y*scale+25,
                                       scale-1, scale-1))
    #for yy in range(3):
    #    for xx in range(3):
    #        px(xx+scale*x, yy+scale*y, (0,0,0))

def draw_x(x, y):
    pxred = lambda x, y: px(x, y, (255,0,0))
    pxred(scale*x+1, scale*y)
    pxred(scale*x+1, scale*y+1)
    pxred(scale*x+1, scale*y+2)
    pxred(scale*x, scale*y+1)
    pxred(scale*x+2, scale*y+1)

def draw_e(x, y, age):
    pxc = lambda x, y: px(x, y, (200,0,200), age)
    pxc(scale*x, scale*y)
    pxc(scale*x+1, scale*y+1)
    pxc(scale*x+2, scale*y+2)
    pxc(scale*x+1, scale*y+3)
    pxc(scale*x, scale*y+4)

def draw_w(x, y, age):
    pxc = lambda x, y: px(x, y, (200,100,0), age)
    pxc(scale*x+3, scale*y)
    pxc(scale*x+2, scale*y+1)
    pxc(scale*x+1, scale*y+2)
    pxc(scale*x+2, scale*y+3)
    pxc(scale*x+3, scale*y+4)

def draw_n(x, y, age):
    pxc = lambda x, y: px(x, y, (100,0,200), age)
    pxc(scale*x+2, scale*y)
    pxc(scale*x+1, scale*y+1)
    pxc(scale*x+3, scale*y+1)
    pxc(scale*x, scale*y+2)
    pxc(scale*x+4, scale*y+2)

def draw_s(x, y, age):
    pxc = lambda x, y: px(x, y, (0,0,200), age)
    pxc(scale*x+2, scale*y+4)
    pxc(scale*x+1, scale*y+3)
    pxc(scale*x+3, scale*y+3)
    pxc(scale*x, scale*y+2)
    pxc(scale*x+4, scale*y+2)

def draw(map, history, pos, status=''):
    [(pg.quit(), sys.exit(0)) for event in pg.event.get() if event.type == pg.QUIT]
    screen.fill((245, 238, 223))

    for y, l in enumerate(status.split('\n')):
        img = font.render(l, True, (0,0,0))
        screen.blit(img, (20, 20+y*25))

    for y, l in enumerate(map):
        for x, c in enumerate(l):
            if (x, y) in history:
                facing, age = history[(x, y)]
                draw_bright(x, y, age)
                if facing == '>':
                    draw_e(x, y, age)
                elif facing == '<':
                    draw_w(x, y, age)
                elif facing == '^':
                    draw_n(x, y, age)
                elif facing == 'v':
                    draw_s(x, y, age)
                #else:
                #    draw_x(x, y)
                #print(history[(x,y)], end='')
            elif c == '#':
                draw_wall(x, y)
            elif c == '.':
                draw_space(x, y)
                #print(c, end='')
        #print()

    # zoomed in display
    x, y = pos
    cropped = pg.Surface((100, 100))
    cropped.blit(screen, (0, 0), (max(x*scale+25-50, 0),
                                  max(y*scale+25-50, 0), 100, 100))
    #cropped.blit(screen, (0, 0), (500, 500, 50, 50))
    zoom = pg.transform.scale(cropped, (200, 200))
    screen.blit(zoom, (50, 100))

    pg.display.flip()
    #clock.tick(2)

def wait_input():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)
            elif event.type == pg.KEYDOWN:
                return

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
        draw(map, history, pos,
             f'facing: {facing}\naction: {action}\nnext: {"".join(path[naction+1:][:1])}')
        #wait_input()

    finalpos, finalfacing = pos, facing
    print(finalpos, finalfacing)
    facev = {'>': 0, 'v': 1, '<':2, '^':3}[finalfacing]
    print(facev)
    print((finalpos[1]+1)*1000 + (finalpos[0]+1)*4 + facev)
    while True:
        draw(map, history, pos)
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
