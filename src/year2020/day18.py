import sys
import re
from yal.util import eval_expr

print(sum(int(eval_expr(line)) for line in sys.stdin.readlines()))
