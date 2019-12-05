#!/usr/bin/env scopes

let min = 168630
let max = 718098
let count = 0

fn six(n)
    true

fn adj(n)
    loop (n prev prev2 prev3 = n -1 -2 -3)
        let this = (n % 10)
        let next = (n // 10)
        if ((this != prev) and (prev == prev2) and (prev2 != prev3))
            break true
        elseif (n >= 10)
            repeat next this prev prev2
        else
            break ((this == prev) and (prev != prev2))

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
        elseif ((six a) and (adj a) and (neverdec a))
            repeat (a + 1) (count + 1)
        else
            repeat (a + 1) count

print "adj"
print (adj 011234) true
print (adj 012234) true
print (adj 012334) true
print (adj 012344) true
print (adj 012345) false
print (adj 222123) false
print (adj 222122) true
print (adj 222144) true
print (adj 220444) true
print (adj 120004) false
print (adj 120004) false

print "neverdec"
print (neverdec 12345) true
print (neverdec 12340) false
print (neverdec 11111) true
print (neverdec 10234) false
print (neverdec 12045) false

print "starting"
print (calc min max)
print "done"
