#!/usr/bin/env ruby

require 'rubygems'
require 'bundler/setup'

require 'gosu'
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
  attr_writer :input

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
          v = @input
          if v.nil?
            raise 'no pls input is nil'
          end
          @program[a] = v
        when 4 # output
          ap = in_param
          if ap.nil?
            raise 'no pls output is nil'
          end
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

class Arcade < Gosu::Window
  attr_reader :screen
  def initialize(initial_program)
    @screen = Hash.new()
    @w = 480
    @h = 320
    #@block_size = 480 / 44
    super @w, @h, false, 1000/10 # 10 fps
    self.caption = "Arcade"

    @initial_program = initial_program
    @initial_program[0] = 2
    @vm = VM.new(initial_program, 0)
    @fib = @vm.run
    puts "starting machine"
    @ball_pos = [0, 0]
    @paddle_pos = [0, 0]
    @font = Gosu::Font.new(20)
  end

  def draw
    @font.draw_text("Score: #{@screen[[-1, 0]]}", 10, 10, 0, 1.0, 1.0, Gosu::Color::YELLOW)
    #canvas = "\n"*25
    #canvas += "Score: #{@screen[[-1, 0]]}\n"
    ball_drawn = false
    (0..23).each { |y|
      (0..43).each { |x|
        map = {
          0 => Gosu::Color::BLACK, # blank
          1 => Gosu::Color::GRAY, # wall
          2 => Gosu::Color::GREEN, # block
          3 => Gosu::Color::BLUE, # paddle
          4 => Gosu::Color::RED # ball
        }
        id = @screen[[x, y]]
        tile = map[id]
        if tile.nil?
          return false
        end
        if id == 4
          ball_drawn = true
        end
        draw_rect(20 + x*10, 40 + y*10, 10, 10, tile)
      }
    }
  end

  def update
    done = false
    while not done
      break if not @fib.alive?
      x = @fib.resume
      break if not @fib.alive?
      y = @fib.resume
      break if not @fib.alive?
      tile = @fib.resume
      #puts [x, y, tile].to_s
      @screen[[x, y]] = tile
      # AI
      if tile == 4
        @ball_pos = [x, y]
        done = true
      end
      if tile == 3
        @paddle_pos = [x, y]
      end
      @vm.input = (@ball_pos[0] > @paddle_pos[0] ? 1 : 0) - (@ball_pos[0] < @paddle_pos[0] ? 1 : 0)
    end
    close if not @fib.alive?
    #if display then
    #  sleep 0.01
    #end
  end

  def close
    score = @screen[[-1, 0]]
    puts score
    super
  end
end

r = Arcade.new(initial_program)
r.show
