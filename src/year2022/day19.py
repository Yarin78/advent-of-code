from dataclasses import dataclass
import sys
from yal.util import *

@dataclass
class BluePrint:
    ore_ore_cost: int
    clay_ore_cost: int
    obs_ore_cost: int
    obs_clay_cost: int
    geode_ore_cost: int
    geode_obs_cost: int

bp = None

max_ore_robs = 0
max_clay_robs = 0
max_obs_robs = 0

memo = {}
def max_geode(ores: int, clay: int, obs: int, num_ore_robs, num_clay_robs, num_obs_robs, minutes_left: int) -> int:
    if minutes_left == 0:
        return 0

    global bp, memo, max_ore_robs, max_clay_robs, max_obs_robs
    assert bp

    key = (ores, clay, obs, num_ore_robs, num_clay_robs, num_obs_robs, minutes_left)
    if key in memo:
        return memo[key]

    new_ores = ores + num_ore_robs
    new_clay = clay + num_clay_robs
    new_obs = obs + num_obs_robs

    best = max_geode(new_ores, new_clay, new_obs, num_ore_robs, num_clay_robs, num_obs_robs, minutes_left - 1)
    if ores >= bp.ore_ore_cost and num_ore_robs < max_ore_robs:
        best = max(best, max_geode(new_ores - bp.ore_ore_cost, new_clay, new_obs, num_ore_robs+1, num_clay_robs, num_obs_robs, minutes_left - 1))
    if ores >= bp.clay_ore_cost and num_clay_robs < max_clay_robs:
        best = max(best, max_geode(new_ores - bp.clay_ore_cost, new_clay, new_obs, num_ore_robs, num_clay_robs+1, num_obs_robs, minutes_left - 1))
    if ores >= bp.obs_ore_cost and clay >= bp.obs_clay_cost and num_obs_robs < max_obs_robs:
        best = max(best, max_geode(new_ores - bp.obs_ore_cost, new_clay - bp.obs_clay_cost, new_obs, num_ore_robs, num_clay_robs, num_obs_robs+1, minutes_left - 1))
    if ores >= bp.geode_ore_cost and obs >= bp.geode_obs_cost:
        best = max(best, minutes_left - 1 + max_geode(new_ores - bp.geode_ore_cost, new_clay, new_obs - bp.geode_obs_cost, num_ore_robs, num_clay_robs, num_obs_robs, minutes_left - 1))

    memo[key] = best
    return best

part1 = 0
part2 = 1
for line in sys.stdin.readlines():
    blueprint_ix, ore_cost, clay_cost, obs_cost1, obs_cost2, geo_cost1, ceo_cost2 = get_ints(line)

    memo = {}
    bp = BluePrint(ore_cost, clay_cost, obs_cost1, obs_cost2, geo_cost1, ceo_cost2)

    max_ore_robs = max(bp.clay_ore_cost, bp.obs_ore_cost, bp.ore_ore_cost)
    max_clay_robs = bp.obs_clay_cost
    max_obs_robs = bp.geode_obs_cost

    gm = max_geode(0, 0, 0, 1, 0, 0, 24)
    print(f"BP {blueprint_ix} can produce {gm} geodes in 24 minutes")

    part1 += blueprint_ix * gm

    if blueprint_ix <= 3:
        gm2 = max_geode(0, 0, 0, 1, 0, 0, 32)
        print(f"BP {blueprint_ix} can produce {gm2} geodes in 32 minutes")
        part2 *= gm2
        if blueprint_ix == 3:
            print("Part 2:", part2)

print("Part 1:", part1)
