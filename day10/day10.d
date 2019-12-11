#!/usr/bin/env rdmd

import std.string;
import std.math;
import std.stdio;
import std.container;

struct Asteroid {
    int x;
    int y;
}

double distance(Asteroid a, Asteroid b) {
    return sqrt(cast(real)pow(a.x - b.x, 2) + cast(real)pow(a.y - b.y, 2));
}

// is b between a and c?
bool between(Asteroid a, Asteroid b, Asteroid c) {
    return distance(a, c) - distance(a, b) + distance(b, c) < 0.0000001;
}

void main() {
    auto asteroids = Array!Asteroid();

    int y = 0;
    foreach (string line; lines(stdin)) {
        line = strip(line);
        int x = 0;
        foreach (char c; line) {
            if (c == '#') {
                asteroids.insertBack(Asteroid(x, y));
            }
            x++;
        }
        y++;
    }
    Asteroid best;
    int best_count = -1;
    foreach (Asteroid potential_base; asteroids) {
        // a is good if there is no b between potential_base and a
        int count=0;
aloop:
        foreach (Asteroid a; asteroids) {
            if (a == potential_base) {
                continue;
            }
            foreach (Asteroid b; asteroids) {
                if (a == b || potential_base == b) {
                    continue;
                }
                if (between(potential_base, b, a)) {
                    //writefln("%s is bad because %s blocks %s", potential_base, b, a);
                    continue aloop;
                }
            }
            count++;
        }
        if (count > best_count) {
            best_count = count;
            best = potential_base;
        }
    }
    writefln("%s %d", best, best_count);
}
