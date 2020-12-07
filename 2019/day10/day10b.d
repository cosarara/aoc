#!/usr/bin/env rdmd

import std.algorithm;
import std.string;
import std.math;
import std.stdio;
import std.container;

struct Asteroid {
    int x;
    int y;
    real angle = 0;
    real distance = 0;
    real rotation = 0;
}

real distance(Asteroid a, Asteroid b) {
    return sqrt(cast(real)pow(a.x - b.x, 2) + cast(real)pow(a.y - b.y, 2));
}

real angle(Asteroid base, Asteroid a) {
    return atan2(cast(real)(base.y - a.y), cast(real)(a.x - base.x));
}

void main() {
    auto asteroids = Array!Asteroid();
    Asteroid base = Asteroid(31, 20);
    //Asteroid base = Asteroid(11, 13);

    int y = 0;
    foreach (string line; lines(stdin)) {
        line = strip(line);
        int x = 0;
        foreach (char c; line) {
            if (c == '#') {
                Asteroid a = Asteroid(x, y);
                if (a != base) {
                    a.distance = distance(base, a);
                    // we rotate clockwise, so we'll count angles clockwise
                    a.angle = -angle(base, a);
                    // we want angle 0 to be pointing up instead of right
                    a.angle += PI/2;
                    // and everything positive
                    if (a.angle < 0) {
                        a.angle += 2*PI;
                    }
                    asteroids.insertBack(a);
                }
            }
            x++;
        }
        y++;
    }

    multiSort!("a.angle < b.angle", "a.distance < b.distance",
            SwapStrategy.unstable)(asteroids[]);
    Asteroid previous = Asteroid(-1, -1, -1);
    foreach (ref a; asteroids) {
        if (a.angle - previous.angle < 0.0001) {
            a.rotation = previous.rotation + 1;
        }
        previous = a;
    }
    multiSort!("a.rotation < b.rotation", "a.angle < b.angle", "a.distance < b.distance",
            SwapStrategy.unstable)(asteroids[]);

    //writefln("%s", asteroids.length());
    //writefln("%s", asteroids[]);
    auto a200 = asteroids[199];
    writefln("%s %d", a200, a200.x*100+a200.y);
}
