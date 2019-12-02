#!/usr/bin/env ruby

inp = $stdin.read
$program = inp.split(",").map{ |x| x.to_i }
$pc = 0

$program[1] = 12
$program[2] = 2

def get_args()
  $program[$pc+1..$pc+4]
end

while true do
  case $program[$pc]
  when 1
    puts 'sum'
    a, b, dest = get_args()
    puts a, b, dest
    $program[dest] = $program[a] + $program[b]
  when 2
    puts 'mul'
    a, b, dest = get_args()
    $program[dest] = $program[a] * $program[b]
  when 99
    puts $program.to_s
    puts 'halt ' + $program[0].to_s
    break
  else
    puts $program.to_s
    puts 'bad bad'
    break
  end
  $pc += 4
end
