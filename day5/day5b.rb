#!/usr/bin/env ruby

inp = $stdin.read
initial_program = inp.split(",").map{ |x| x.to_i }

def read_int
  if ARGV[0] != nil
    return ARGV[0].to_i
  else
    return 1
  end
end

def write_int x
  puts "OUTPUT:", x
end

def run(program)
  pc = 0

  while program[pc] != 99 do
    instruction = program[pc]
    op = instruction % 100
    #puts "PC " + pc.to_s + " OP " + op.to_s
    instruction /= 100
    a, b, c = program[pc+1..pc+4]
    ap, bp, cp = a, b, c

    if instruction % 10 == 0
      ap = program[a]
    end
    instruction /= 10
    if instruction % 10 == 0
      bp = program[b]
    end

    case op
    when 1 # add
      program[c] = ap + bp
      pc += 4
    when 2 # mul
      program[c] = ap * bp
      pc += 4
    when 3 # input
      program[a] = read_int
      pc += 2
    when 4 # output
      write_int(ap)
      pc += 2
    when 5 # jit
      if ap != 0
        pc = bp
      else
        pc += 3
      end
    when 6 # jif
      if ap == 0
        pc = bp
      else
        pc += 3
      end
    when 7 # lt
      program[c] = ap < bp ? 1 : 0
      pc += 4
    when 8 # eq
      program[c] = ap == bp ? 1 : 0
      pc += 4
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
