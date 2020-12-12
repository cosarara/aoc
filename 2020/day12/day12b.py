import pygame
from math import pi
import sys

nodraw = '--nodraw' in sys.argv

pygame.init()

if not nodraw:
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    myfont = pygame.font.SysFont('monospace', 20)
    shipw = pygame.image.load("ship.png")
    shipe =  pygame.transform.flip(shipw, True, False)
    shipn =  pygame.transform.rotate(shipw, -90)
    ships =  pygame.transform.rotate(shipw, 90)
    zoom = 0.1

with open('input') as f:
    inp = f.read().strip().split('\n')

def draw(x, y, wx, wy, px, py, l, f, angles=None):
    if nodraw:
        return
    screen.fill((255, 255, 255))
    shipcol = (255, 0, 0)
    drawx = width // 2
    drawy = 400
    #drawy = height // 2
    black = (0, 0, 0)
    pygame.draw.line(screen, black,
                     (-1000+drawx, drawy),
                     (1000+drawx, drawy))
    pygame.draw.line(screen, black,
                     (drawx, -1000+drawy),
                     (drawx, 1000+drawy))
    # -y because for pygame positive y is down
    zoom = min(0.3 / max(abs(x) / width, abs(y) / height), 1)
    transform = lambda x, y: (x*zoom+drawx, -y*zoom+drawy)
    sx, sy = transform(x, y)
    spx, spy = transform(px, py)
    pygame.draw.line(screen, black,
                     (spx, spy),
                     (sx, sy))

    if angles:
        d2r = lambda d : pi * (d/180)
        pang, nang = start_angle, stop_angle = angles
        if (stop_angle < start_angle):
            stop_angle, start_angle = start_angle, stop_angle
        pygame.draw.arc(screen, (0, 255, 0),
                        (sx-100, sy-100, 200, 200),
                        d2r(start_angle), d2r(stop_angle))
        ship = pygame.transform.rotate(shipe, nang)
        shiprect = (sx-4, sy-4, 8, 8)
        screen.blit(ship, shiprect)

    else:
        # -4 because the rect is 8x8
        shiprect = (sx-4, sy-4, 8, 8)
        ship = {'W': shipw, 'E': shipe, 'N': shipn,
                'S': ships}[f]
        screen.blit(ship, shiprect)

    swx, swy = transform(wx*10+x, wy*10+y)
    pygame.draw.circle(screen, black,
                     (swx, swy),
                     4, 0)

    for i in range(100):
        ax, ay = transform(i * 500, 0)
        pygame.draw.circle(screen, black,
                         (ax, ay),
                         2, 0)
        ax, ay = transform(0, i * 500)
        pygame.draw.circle(screen, black,
                         (ax, ay),
                         2, 0)

    lsurf = myfont.render(l, False, black)
    screen.blit(lsurf, (20, height-120))
    psurf = myfont.render(str((x, y, f)), False, black)
    screen.blit(psurf, (20, height-100))
    dsurf = myfont.render("dist: "+str(abs(x)+abs(y)),
                          False, black)
    screen.blit(dsurf, (20, height-80))
    pygame.display.flip()
    #pygame.time.wait(150)

x = 0
y = 0
wx = 10
wy = 1
f = 'E' # we start facing east
for l in inp:
    #print('\n'*50)
    print(l, x, y, wx, wy)
    a = l[0]
    b = int(l[1:])
    px, py = x, y
    if a == 'F':
        for i in range(b):
            x += wx
            y += wy
            draw(x, y, wx, wy, px, py, l, f)
            if not nodraw:
                pygame.time.wait(50)
        continue
    ang = {'W': 180, 'N': 90, 'E': 0, 'S': 270}
    face = {v: k for k, v in ang.items()}
    v = (0, 0)
    if a == 'R':
        for i in range(b // 90):
            wx, wy = wy, -wx
            draw(x, y, wx, wy, px, py, l, f)
            if not nodraw:
                pygame.time.wait(50)
        continue
    if a == 'L':
        for i in range(b // 90):
            wx, wy = -wy, wx
            draw(x, y, wx, wy, px, py, l, f)
            if not nodraw:
                pygame.time.wait(50)
        continue
    if a == 'N':
        v = (0, 1)
    elif a == 'S':
        v = (0, -1)
    elif a == 'E':
        v = (1, 0)
    elif a == 'W':
        v = (-1, 0)
    dx, dy = v
    for i in range(b):
        wx += dx
        wy += dy
        draw(x, y, wx, wy, px, py, l, f)
        if not nodraw:
            pygame.time.wait(50)
    #dx *= b
    #dy *= b
    #x += dx
    #y += dy

    print(l, x, y, wx, wy)
    draw(x, y, wx, wy, px, py, l, f)
    #pygame.time.wait(50)

print(x, y, abs(x)+abs(y))
