import sys
from collections import defaultdict
from lib import util
from queue import Queue
#from aocd import data, submit

# Make sure AOC_SESSION is updated! (Chrome inspector -> Application tab -> session)

code = '1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,6,19,1,5,19,23,1,23,6,27,1,5,27,31,1,31,6,35,1,9,35,39,2,10,39,43,1,43,6,47,2,6,47,51,1,5,51,55,1,55,13,59,1,59,10,63,2,10,63,67,1,9,67,71,2,6,71,75,1,5,75,79,2,79,13,83,1,83,5,87,1,87,9,91,1,5,91,95,1,5,95,99,1,99,13,103,1,10,103,107,1,107,9,111,1,6,111,115,2,115,13,119,1,10,119,123,2,123,6,127,1,5,127,131,1,5,131,135,1,135,6,139,2,139,10,143,2,143,9,147,1,147,6,151,1,151,13,155,2,155,9,159,1,6,159,163,1,5,163,167,1,5,167,171,1,10,171,175,1,13,175,179,1,179,2,183,1,9,183,0,99,2,14,0,0'

for noun in range(100):
    for verb in range(100):
        program = util.get_ints(code)

        program[1] = noun
        program[2] = verb

        pc = 0
        while True:
            if program[pc] == 1:
                program[program[pc+3]] = program[program[pc+1]] + program[program[pc+2]]
            elif program[pc] == 2:
                program[program[pc+3]] = program[program[pc+1]] * program[program[pc+2]]
            elif program[pc] == 99:
                break
            else:
                assert False
            pc += 4
            #print(program)

        #print(program[0])
        if(program[0] == 19690720):
            print(100*noun+verb)


        # submit(cnt, part="a", day=2, year=2019)
