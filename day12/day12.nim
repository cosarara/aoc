# every little thing I think I'll want to do requires a fucking import
# I thought the python docs were bad, but this is next level bad
# there are no examples, anywhere
# just stupid function signatures
# I DON'T WANT TO READ SIGNATURES UNLESS I HAVE A BUG
# SIGNATURES ARE FOR THE COMPILER TO READ
#import strformat
import strutils
import sequtils

#let lines = split(input, '\n')
# errors on this language suck
var positions : array[4, array[3, int]]
var velocities : array[4, array[3, int]]

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

for step in 1..10:
  for i in 0..2: # coord
    for j in 0..3: # moon
      for k in 0..3: # other moon
        velocities[j][i] += (if positions[j][i] < positions[k][i]: 1 else: 0) -
                            (if positions[j][i] > positions[k][i]: 1 else: 0);
    for j in 0..3: # moon
      positions[j][i] += velocities[j][i]
  var energy = 0
  for j in 0..3: # moon
  #  echo j
    let pot = (positions[j].foldl(abs(a) + abs(b)))
    let kin = (velocities[j].foldl(abs(a) + abs(b)))
    energy += pot * kin
  #  echo "pot ", pot
  #  echo "kin ", kin
  #  echo "en ", pot * kin
  echo step, " ", energy
  echo step, " ", positions
  echo step, " ", velocities
