#!/usr/bin/env ruby

require 'fiber'

inp = $stdin.read
initial_program = inp.split(",").map{ |x| x.to_i }

def write_int x
  puts "OUTPUT:", x
end

class VM
  attr_reader :input

  def in_param
    a = out_param
    if @instruction % 10 == 0
      a = @program[a]
    end
    @instruction /= 10
    a
  end

  def out_param
    a = @program[@pc]
    @pc += 1
    a
  end

  def read_int
    #puts "reading input"
    @input.shift
  end

  def initialize(program, input)
    @program = program.clone
    @input = input
    @output = []
    @pc = 0
    @instruction = 0
  end

  def halted
    @program[@pc] == 99
  end

  def run
    fiber = Fiber.new do
      #puts "running " + @program[@pc].to_s
      while not halted do
        pc = @pc
        @instruction = out_param
        op = @instruction % 100
        #puts "PC " + pc.to_s + " OP " + op.to_s
        @instruction /= 100

        case op
        when 1 # add
          ap = in_param
          bp = in_param
          c = out_param
          @program[c] = ap + bp
        when 2 # mul
          ap = in_param
          bp = in_param
          c = out_param
          @program[c] = ap * bp
        when 3 # input
          a = out_param
          @program[a] = read_int
        when 4 # output
          ap = in_param
          @input.push(Fiber.yield ap)
        when 5 # jit
          ap = in_param
          bp = in_param
          if ap != 0
            @pc = bp
          end
        when 6 # jif
          ap = in_param
          bp = in_param
          if ap == 0
            @pc = bp
          end
        when 7 # lt
          ap = in_param
          bp = in_param
          c = out_param
          @program[c] = ap < bp ? 1 : 0
        when 8 # eq
          ap = in_param
          bp = in_param
          c = out_param
          @program[c] = ap == bp ? 1 : 0
        else
          puts 'bad bad'
          puts 'pc ' + @pc.to_s
          puts 'in ' + @program[@pc].to_s
          puts 'op ' + op.to_s
          puts @program.to_s
          break
        end
      end
      false
    end
    fiber
  end
end

base_phase = [5, 6, 7, 8, 9]
max_out = 0
max_phase = []
for phase in base_phase.permutation do
  prev = 0
  vms = []
  for num in phase do
    vm = VM.new(initial_program, [num, prev]).run
    vms.push(vm)
    prev = vm.resume
  end
  while vms[0].alive? do
    for vm in vms do
      prev = (vm.resume prev) || prev
    end
  end
  if prev > max_out
    max_out = prev
    max_phase = phase
  end
end
puts "MAX"
puts max_out, max_phase.to_s
