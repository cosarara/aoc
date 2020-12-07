#!/usr/bin/env ruby

require 'rubygems'
require 'bundler/setup'

require 'gosu'
require 'fiber'
require 'pry'

#inp = $stdin.read
file = File.open("input.txt")
inp = file.read
initial_program = inp.split(",").map{ |x| x.to_i }

class Memory < Array
  def [](a)
    v = super(a)
    v || 0
  end
end

class VM
  attr_accessor :input

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
    @w = 500
    @h = 500
    #@block_size = 480 / 44
    super @w, @h, false, 1000/60 # fps
    self.caption = "Arcade"

    @initial_program = initial_program
    @vm = VM.new(initial_program, nil)
    @fib = @vm.run
    puts "starting machine"
    @x = 25
    @y = 25
    @font = Gosu::Font.new(20)
    @direction = nil
    explore
  end

  def dirmap(dir, x, y)
    {
      1 => [x, y-1],
      2 => [x, y+1],
      3 => [x-1, y],
      4 => [x+1, y],
    }[dir]
  end

  def draw
    (0..50).each { |y|
      (0..50).each { |x|
        id = @screen[[x, y]]
        map = {
        #  0 => Gosu::Color::ORANGE, # robot
        #  1 => Gosu::Color::GREEN, # block
        #  2 => Gosu::Color::CYAN, # paddle
        #  4 => Gosu::Color::RED # ball
          0 => Gosu::Color::GRAY, # wall
          1 => Gosu::Color::WHITE, # walkable
          2 => Gosu::Color::FUCHSIA, # oxigen
        }
        tile = map[id]
        draw_rect(x*10, y*10, 10, 10, tile) if tile
      }
    }
    draw_rect(@x*10, @y*10, 10, 10, Gosu::Color::BLUE)
    if @endpath then
      (x, y) = [25, 25]
      for dir in @endpath
        (x2, y2) = dirmap(dir, x, y)
        c = Gosu::Color.argb(0xff_ff0088);
        draw_line(x*10+5, y*10+5, c, x2*10+5, y2*10+5, c)
        (x, y) = [x2, y2]
      end
    end
  end

  def button_down(id)
    case id
    when Gosu::KbEscape
      close
    when Gosu::KbUp
      @direction = 1
    when Gosu::KbDown
      @direction = 2
    when Gosu::KbLeft
      @direction = 3
    when Gosu::KbRight
      @direction = 4
    when Gosu::KB_Z
      binding.pry
    #when Gosu::KB_SPACE
    #  path = astar([@x, @y], nil)
    #  puts path[0]
    #  move(path[0])
    end
  end

  def opposite(dir)
    {
      1 => 2,
      2 => 1,
      3 => 4,
      4 => 3
    }[dir]
  end

  def move(input)
    @vm.input = input
    res = @fib.resume
    (x, y) = dirmap(@vm.input, @x, @y);
    #puts [@x, @y, x, y].to_s
    @vm.input = nil;
    if res == 0 then
      @screen[[x, y]] = 0
    elsif res == 1 then # succeeded
      @screen[[x, y]] = 1
      @x = x
      @y = y
    else # succeeded and found objective
      @end = [x, y]
      @screen[[x, y]] = 2
      @x = x
      @y = y
      @endpath = astar([25, 25], @end)
      puts @endpath.to_s
      puts @endpath.length
    end
    res
  end

  def try(input)
    #puts input
    if move(input) != 0 then
      move(opposite(input))
    end
  end

  def nilneighbors?(pos)
    x, y = pos
    [[x, y+1], [x, y-1], [x+1, y], [x-1, y]].any? {
      |pos| @screen[pos] == nil
    }
  end

  def neighbors(pos)
    x, y = pos
    [[x, y+1], [x, y-1], [x+1, y], [x-1, y]].filter {
      |pos| @screen[pos] == 1 || @screen[pos] == 2
    }
  end

  def astar(pstart, pend)
    frontier = Queue.new
    frontier.push(pstart)
    came_from = {}
    came_from[pstart] = nil
    dist = {}
    dist[pstart] = 0

    while not frontier.empty? do
      #puts ["l", frontier.length].to_s
      curr = frontier.pop()
      if pend == nil and nilneighbors?(curr) then
        pend = curr
      end
      #puts ["neigh", neighbors(curr)].to_s
      for pnext in neighbors(curr) do
        if not came_from.key?(pnext) then
          frontier.push(pnext)
          came_from[pnext] = curr
          dist[pnext] = dist[curr] + 1
        end
      end
      #puts ["hrm", came_from, curr].to_s
    end
    if not pend
      puts dist.values.max
      return
    end
    curr = pend
    if came_from[curr].nil?
      binding.pry
    end
    path = []
    while curr != pstart do
      diff = curr.zip(came_from[curr]).map {|a, b| a-b}
      dir = {
        [0, -1] => 1,
        [0, 1] => 2,
        [-1, 0] => 3,
        [1, 0] => 4,
      }[diff]
      path.unshift(dir)
      curr = came_from[curr]
    end
    path
  end

  def explore
    (1..4).each{ |n| try(n) }
  end

  def update
    if @direction then
      puts @direction
      while move(@direction) == 1 and button_down?(Gosu::KB_LEFT_SHIFT) do
        explore
      end
      explore
      @direction = nil
    elsif button_down?(Gosu::KB_SPACE)
      path = astar([@x, @y], nil)
      if path and not path.empty?
        #puts path.to_s
        move(path[0])
        explore
      end
      if path.nil?
        astar(@end, nil)
      end
    end
  end

  def close
    score = @screen[[-1, 0]]
    puts score
    super
  end
end

r = Arcade.new(initial_program)
r.show
