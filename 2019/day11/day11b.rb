#!/usr/bin/env ruby

require 'fiber'

inp = $stdin.read
initial_program = inp.split(",").map{ |x| x.to_i }

class Memory < Array
  def [](a)
    v = super(a)
    v || 0
  end
end

class VM
  attr_reader :input

  def in_param
    a = @program[@pc]
    @pc += 1
    # 0 = position mode
    # 1 = immediate mode
    # 2 = relative mode
    if @instruction % 10 == 0
      a = @program[a]
    elsif @instruction % 10 == 2
      a = @program[@rb+a]
    end
    @instruction /= 10
    a
  end

  def out_param
    a = @program[@pc]
    @pc += 1
    if @instruction % 10 == 2
      a += @rb
    end
    @instruction /= 10
    a
  end

  def initialize(program, input)
    @program = Memory.new(program.clone)
    @input = input
    @output = []
    @pc = 0
    @rb = 0 # relative base
    @instruction = 0
  end

  def halted
    @program[@pc] == 99
  end

  def run
    fiber = Fiber.new do
      #puts "running " + @program[@pc].to_s
      while not halted do
        @instruction = out_param
        op = @instruction % 100
        #puts "PC #{@pc.to_s} RB #{@rb} INSTRUCTION #{@instruction} OP #{op.to_s}"
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
          #puts "    intcode requesting input"
          v = Fiber.yield
          #puts "    intcode got #{v}"
          if v.nil?
            raise 'no pls input is nil'
          end
          @program[a] = v
        when 4 # output
          ap = in_param
          if ap.nil?
            raise 'no pls output is nil'
          end
          #@input.push(Fiber.yield ap)
          #puts "    intcode outputting #{ap}"
          if not (Fiber.yield ap).nil? then
            raise "I didn't expect input here"
          end
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
        when 9 # rb adjust
          ap = in_param
          @rb += ap
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

class Robot
  attr_reader :colors
  def initialize()
    @colors = Hash.new()
    @right_rotation = [:up, :right, :down, :left];
  end

  def run(initial_program)
    direction = :up;
    x = 50
    y = 17
    @colors[[x, y]] = 1
    vm = VM.new(initial_program, []).run
    puts "starting machine"
    while vm.alive?
      vm.resume
      break if not vm.alive?
      color = @colors[[x, y]] || 0
      new_color = vm.resume color
      @colors[[x, y]] = new_color
      dir = vm.resume
      shift = dir * 2 - 1
      i = @right_rotation.find_index(direction)+shift
      if i == 4
        i = 0
      end
      direction = @right_rotation[i]
      x += {:up => 0, :down => 0, :right => 1, :left => -1}[direction];
      y += {:up => -1, :down => 1, :right => 0, :left => 0}[direction];
    end
  end
end

r = Robot.new()
r.run(initial_program)
puts r.colors.keys.length
#puts r.colors
#
#r.colors.each { |k,c| puts k.to_s if c }

canvas = ""
(1..70).each { |y|
  (1..120).each { |x|
    canvas += r.colors[[x, y]] == 1 ? "X" : " "
  }
  canvas += "\n"
}
puts canvas
