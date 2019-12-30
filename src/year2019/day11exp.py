from collections import defaultdict
from lib.geo2d import *
from lib import util

class Program:
    def __init__(self, output):
        self._output = output

    def input(self):
        return 0

    def output(self, v):
        self._output.put(v)

    def run(self):
        self.output(0)
        self.output(1)
        self.func451(937263411860)
        self.func451(932440724376)
        self.input()
        self.output(0)
        self.output(1)
        self.input()
        self.output(0)
        self.output(0)
        self.input()
        self.output(0)
        self.output(1)
        self.input()
        self.output(0)
        self.output(1)
        self.input()
        self.output(0)
        self.output(0)
        self.input()
        self.output(0)
        self.output(1)
        self.func451(29015167015)
        self.func451(3422723163)
        self.input()
        self.output(0)
        self.output(0)
        self.input()
        self.output(0)
        self.output(0)
        self.func451(868389376360)
        self.func451(825544712960)

    def func451(self, code):
        self.func515(code, 40, 482)

    def func515(self, code, bits, addr):
        # addr is the address of the paint function
        if code < 0:  # testing overflow perhaps!?
            code = 0
        self.unpack(code, bits, 1)

    counter = 0
    dirs = [1, 0, 0, 1]

    def paint_it(self, p0):
        self.input()
        self.output(p0)
        self.output(self.dirs[self.counter])
        self.counter = (self.counter + 1) % 4

    # each bit in code represents a pixel
    # paints the most significant pixel first by means of "headrecursion"
    def unpack(self, code, left, mask):
        # mask = a power of two
        # code = what's left the paint
        # left = pixels left to paint
        if left < 1 and code < mask:
            return code

        code = self.unpack(code, left-1, mask*2)

        color = 1
        if mask > code:
            color = 0
            mask = 0
        if left > 0:  # this check is not necessary
            self.paint_it(color)

        return code - mask



DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

map = defaultdict(int)
dir = 0
pos = Point(0,0)

class Painter:
    p = 0

    def put(self, v):
        global dir, pos, map
        if self.p == 0:
            map[pos] = v
            self.p = 1
        elif self.p == 1:
            if v == 0:
                dir = (dir+3)%4
            else:
                dir = (dir+1)%4
            pos += DIRECTIONS[dir]
            self.p = 0

p = Program(Painter())
p.run()
util.print_array(util.gridify_sparse_map(map))
