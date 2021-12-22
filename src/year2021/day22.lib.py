import sys
from yal.util import *
from yal.geo3d import *


blocks = []
for line in sys.stdin.readlines():
    x1,x2,y1,y2,z1,z2 = get_ints(line)
    blocks.append((Block(Point(x1,y1,z1), Point(x2+1,y2+1,z2+1)), line.startswith("on")))

def count_rec(block: Block, current: int):
    if current == len(blocks):
        return block.volume()
    
    sum = 0
    for sub_block in block.subtract(blocks[current][0]):
        sum += count_rec(sub_block, current+1)
    return sum    

print(sum(count_rec(block, i+1) for i, (block, state) in enumerate(blocks) if state))
