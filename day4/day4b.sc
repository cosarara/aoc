#!/usr/bin/env scopes

let min = 168630
let max = 718098
let count = 0

fn six(n)
    true

fn adj(n)
    loop (n prev = n -1)
        let this = (n % 10)
        let next = (n // 10)
        if (this == prev)
            break true
        elseif (n >= 10)
            repeat next this
        else
            break false

fn adj3(n)
    loop (n prev prev2 = n -1 -2)
        let this = (n % 10)
        let next = (n // 10)
        if ((this == prev) and (prev == prev2))
            break true
        elseif (n >= 10)
            repeat next this prev
        else
            break false

fn neverdec(n)
    loop (n prev = n 10)
        let this = (n % 10)
        let next = (n // 10)
        if (this > prev)
            break false
        elseif (n >= 10)
            repeat next this
        else
            break true

fn calc(min max)
    loop (a count = min 0)
        if (a >= max)
            print "finished"
            print count
            break a count
        elseif ((six a) and (adj a) and (neverdec a) and (not (adj3 a)))
            repeat (a + 1) (count + 1)
        else
            repeat (a + 1) count

print "adj"
print (adj 11234) true
print (adj 12234) true
print (adj 12334) true
print (adj 12344) true
print (adj 12345) false

print "neverdec"
print (neverdec 12345) true
print (neverdec 12340) false
print (neverdec 11111) true
print (neverdec 10234) false
print (neverdec 12045) false

print "adj3"
print (adj3 11133) true
print (adj3 11233) false
print (adj3 11333) true
print (adj3 33333) true
print (adj3 13331) true
print (adj3 13321) false

print "starting"
print (calc min max)
print "done"
