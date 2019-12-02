#!/usr/bin/env ruby

inp = $stdin.read
program = inp.split(",").map{ |x| x.to_i }
initial_program = program.clone
pc = 0

noun = 0
verb = 0

loop do
  program = initial_program.clone
  program[1] = noun
  program[2] = verb

  while program[pc] != 99 do
    case program[pc]
    when 1
      #puts 'sum'
      a, b, dest = program[pc+1..pc+4]
      #puts a, b, dest
      program[dest] = program[a] + program[b]
    when 2
      #puts 'mul'
      a, b, dest = program[pc+1..pc+4]
      program[dest] = program[a] * program[b]
    else
      puts program.to_s
      puts 'bad bad'
      break
    end
    pc += 4
  end
  #puts program.to_s
  puts 'halt ' + program[0].to_s, noun, verb if program[0] != 1
  if program[0] == 19690720 then
    puts 'yay', noun, verb, 100 * noun + verb
    break
  end
  noun += 1
  if noun > 99 then
    noun = 0
    verb += 1
  end
  if verb > 99 then
    puts 'no pls'
    break
  end
  # I missed this at first and I felt quite stupid tbh
  pc = 0
end
