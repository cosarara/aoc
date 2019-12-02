#!/usr/bin/env ruby

inp = $stdin.read
initial_program = inp.split(",").map{ |x| x.to_i }

def run(program, noun, verb)
  program[1] = noun
  program[2] = verb
  pc = 0

  while program[pc] != 99 do
    case program[pc]
    when 1
      a, b, dest = program[pc+1..pc+4]
      program[dest] = program[a] + program[b]
    when 2
      a, b, dest = program[pc+1..pc+4]
      program[dest] = program[a] * program[b]
    else
      puts program.to_s
      puts 'bad bad'
      break
    end
    pc += 4
  end
  program
end

noun = 0
verb = 0
loop do
  program = run(initial_program.clone, noun, verb)
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
end
