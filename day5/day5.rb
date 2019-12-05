#!/usr/bin/env ruby

inp = $stdin.read
initial_program = inp.split(",").map{ |x| x.to_i }

def read_int
  1
end

def write_int x
  puts "OUTPUT:", x
end

def run(program)
  pc = 0

  while program[pc] != 99 do
    instruction = program[pc]
    op = instruction % 100
    instruction /= 100
    a, b, c = program[pc+1..pc+4]
    case op
    when 1
      if instruction % 10 == 0
        a = program[a]
      end
      instruction /= 10
      if instruction % 10 == 0
        b = program[b]
      end
      program[c] = a + b
      pc += 4
    when 2
      if instruction % 10 == 0
        a = program[a]
      end
      instruction /= 10
      if instruction % 10 == 0
        b = program[b]
      end
      program[c] = a * b
      pc += 4
    when 3
      program[a] = read_int
      pc += 2
    when 4
      if instruction % 10 == 0
        a = program[a]
      end
      write_int(a)
      pc += 2
    else
      puts 'bad bad'
      puts 'pc ' + pc.to_s
      puts 'in ' + program[pc].to_s
      puts 'op ' + op.to_s
      puts program.to_s
      break
    end
  end
  program
end

run(initial_program)
