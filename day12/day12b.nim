# every little thing I think I'll want to do requires a fucking import
# I thought the python docs were bad, but this is next level bad
# there are no examples, anywhere
# just stupid function signatures
# I DON'T WANT TO READ SIGNATURES UNLESS I HAVE A BUG
# SIGNATURES ARE FOR THE COMPILER TO READ
#import strformat
import strutils
import sequtils
import math

#let lines = split(input, '\n')
# errors on this language suck
var ipositions : array[4, array[3, int]]
var positions : array[4, array[3, int]]
var velocities : array[4, array[3, int]]
var loops : array[3, int]

var i = 0
# streams dont implement pairs() (enumerate)
for tainted_line in lines(stdin):
  let line = tainted_line.string.strip(chars = {'<', '>'})
  let parts = line.split(", ")
  # but arrays do
  for j, part in parts:
    let xv = part.split("=")
    positions[i][j] = parseInt(xv[1])
  i += 1

ipositions = positions

for i in 0..2: # coord
  for step in 1..10000000:
    for j in 0..3: # moon
      for k in 0..3: # other moon
        velocities[j][i] += (if positions[j][i] < positions[k][i]: 1 else: 0) -
                            (if positions[j][i] > positions[k][i]: 1 else: 0);
    var all_eq = true
    var all_zero = true
    for j in 0..3: # moon
      positions[j][i] += velocities[j][i]
      if positions[j][i] != ipositions[j][i]:
        all_eq = false
      if velocities[j][i] != 0:
        all_zero = false
    if all_eq and all_zero:
      #echo "yay", step, " ", positions, " ", ipositions
      loops[i] = step
      break

#echo lcm(loops[0], lcm(loops[1], loops[2]))
echo loops.foldl(lcm(a, b)) # magic a and b instead of foldl(lcm) what is this
