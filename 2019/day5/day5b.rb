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

class VM
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

  def initialize(program)
    @program = program
    @pc = 0
    @instruction = 0

    while @program[@pc] != 99 do
      pc = @pc
      @instruction = out_param
      op = @instruction % 100
      puts "PC " + pc.to_s + " OP " + op.to_s
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
        program[a] = read_int
      when 4 # output
        ap = in_param
        write_int(ap)
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
        program[c] = ap < bp ? 1 : 0
      when 8 # eq
        ap = in_param
        bp = in_param
        c = out_param
        program[c] = ap == bp ? 1 : 0
      else
        puts 'bad bad'
        puts 'pc ' + @pc.to_s
        puts 'in ' + @program[@pc].to_s
        puts 'op ' + op.to_s
        puts @program.to_s
        break
      end
    end
    @program
  end
end

VM.new(initial_program)
