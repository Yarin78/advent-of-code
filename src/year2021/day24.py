import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]

instr = [line.split(' ') for line in lines]

cache = {}

def check(ip, w, x, y, z, inps):
    #print(f"@{ip}  w={w} x={x} y={y} z={z}")
    if ip == len(instr):
        return "" if z == 0 else None
    regs = [w, x, y, z]
    cur = instr[ip]
    #print(cur)
    if cur[0] == "inp":
        assert cur[1] == "w"
        if z > 26**(14-inps):
            return None
        key = (inps, z)
        if key in cache:
            return cache[key]
        for i in range(9,0,-1):
        #for i in range(1, 10):
            if inps == 1:
                print(i)
            v=check(ip+1, i, x, y, z, inps+1)
            if v is not None:
                cache[key] = str(i) + v
                return str(i) + v
        
        cache[key] = None
        return None
    else:
        a = regs[ord(cur[1])-119]
        if is_int(cur[2]):
            b = int(cur[2])
        else:
            b = regs[ord(cur[2])-119]
            
        # print(cur[0], a, b)
        if cur[0] == "add":
            a += b
        elif cur[0] == "mul":
            a *= b
        elif cur[0] == "div":
            if b == 0:
                return None
            if a >= 0:
                a //= b
            else:
                a = (a+1) // b
        elif cur[0] == "mod":
            if a < 0 or b <= 0:
                return None
            a %= b
        elif cur[0] == "eql":
            a = 1 if a == b else 0
        else:
            #print(cur[0])
            assert False
        
        regs[ord(cur[1])-119] = a
        #print(regs)
        return check(ip+1, regs[0], regs[1], regs[2], regs[3], inps)
   

    
print(check(0, 0, 0, 0, 0, 0))

def conv(instr):
    inp_no = 0
    for cur in instr:
        if cur[0] == "inp":
            a = cur[1]
            print(f"{a} = get_input({inp_no})")
            inp_no += 1
        else:
            a = cur[1]
            b = cur[2]        
            if cur[0] == "add":
                print(f"{a} += {b}")
            elif cur[0] == "mul":
                print(f"{a} *= {b}")
            elif cur[0] == "div":
                print(f"{a} = {a} // {b} if {a} >= 0 else ({a}+1)//{b}")
            elif cur[0] == "mod":
                print(f"{a} %= {b}")
            elif cur[0] == "eql":
                print(f"{a} = int({a} == {b})")
