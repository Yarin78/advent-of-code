from dataclasses import dataclass
import sys
from yal.io import *
from yal.util import *
from yal.grid import *
from yal.graph import *
from yal.geo2d import *

lines = [line.strip() for line in sys.stdin.readlines()]
sections = split_lines(lines)

@dataclass
class Rule:
    var: str
    val: int
    op: str
    target: str  # R, A or name

@dataclass
class Workflow:
    name: str
    rules: List[Rule]
    default_dest: str

workflows: Dict[str, Workflow] = {}

for line in sections[0]:
    workflow_name, rule_expr = line.split('{')
    rule_expr = rule_expr[:-1]
    rules = rule_expr.split(',')
    workflow = []

    done = False
    for rulefull in rules:
        assert not done
        if ':' in rulefull:
            rule, dest = rulefull.split(':')
            if '<' in rule:
                var, val = rule.split('<')
                val = int(val)
                op = '<'
            elif '>' in rule:
                var, val = rule.split('>')
                val = int(val)
                op = '>'
            else:
                assert False
            workflow.append(Rule(var, val, op, dest))
        else:
            workflows[workflow_name] = Workflow(workflow_name, workflow, rulefull)
            done = True


def check(part: Dict[str, int], wid: str) -> bool:
    wf = workflows[wid]
    for rule in wf.rules:
        matches = (rule.op == '<' and part[rule.var] < rule.val) or (rule.op == '>' and part[rule.var] > rule.val)
        if matches:
            if rule.target == 'A':
                return True
            if rule.target == 'R':
                return False
            return check(part, rule.target)
    if wf.default_dest == 'A':
        return True
    if wf.default_dest == 'R':
        return False
    return check(part, wf.default_dest)


def accept(part: Dict[str, Tuple]) -> int:
    mult = 1
    for rmin, rmax in part.values():
        mult *= (rmax-rmin+1)
    return mult

def check_range(part: Dict[str, Tuple], wid: str) -> int:
    answer = 0
    wf = workflows[wid]
    for rule in wf.rules:
        oldmin, oldmax = part[rule.var]
        if rule.op == '<':
            matchmin = min(oldmin, rule.val-1)
            matchmax = min(oldmax, rule.val-1)
        else:
            matchmin = max(oldmin, rule.val+1)
            matchmax = max(oldmax, rule.val+1)

        if matchmin <= matchmax:
            new_part = {**part, rule.var:(matchmin, matchmax)}
            if rule.target == 'A':
                answer += accept(new_part)
            elif rule.target != 'R':
                answer += check_range(new_part, rule.target)

        if rule.op == '<':
            # Must be >=
            nomatchmin = max(oldmin, rule.val)
            nomatchmax = max(oldmax, rule.val)
        else:
            # Must be <=
            nomatchmin = min(oldmin, rule.val)
            nomatchmax = min(oldmax, rule.val)

        part = {
            **part,
            rule.var: (nomatchmin, nomatchmax)
        }
        if nomatchmin > nomatchmax:
            return answer

    if wf.default_dest == 'A':
        answer += accept(part)
    elif wf.default_dest != 'R':
        answer += check_range(part, wf.default_dest)
    return answer

part1 = 0
for part in sections[1]:
    values = part[1:-1].split(',')
    p = {}
    for val in values:
        var, v = val.split('=')
        v = int(v)
        p[var] = v

    if check(p, "in"):
        part1 += sum(p.values())

print(part1)
print(check_range({c: (1, 4000) for c in 'xmas'}, "in"))
