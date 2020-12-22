import sys
from queue import Queue
from collections import defaultdict
from itertools import permutations
from yal.util import *
from yal.graph import *
from yal.geo2d import *
from vm.vm import *

# Make sure ~/.config/aocd/token is correct! (Chrome inspector -> Application tab -> Cookies)
lines = [line.strip() for line in sys.stdin.readlines()]

foods = []
allergen_foods = {}
ing_foods = {}
cur_food = 0
for line in lines:
    if ' (contains' in line:
        parts = line.split(' (contains')
        ingredients = parts[0].split(' ')
        allergens = parts[1].rstrip(')').strip().split(' ')
        allergens = [a.strip(',') for a in allergens]
    else:
        ingredients = line.split(' ')
        allergens = []
    for a in allergens:
        assert '(' not in a
        assert ' ' not in a
    for i in ingredients:
        assert '(' not in i
        assert ' ' not in i
    foods.append(ingredients)
    for a in allergens:
        if a not in allergen_foods:
            allergen_foods[a] = []
        allergen_foods[a].append(cur_food)
    for i in ingredients:
        if i not in ing_foods:
            ing_foods[i] = []
        ing_foods[i].append(cur_food)
    #print(ingredients, allergens)
    cur_food += 1


all_allergens = []
allergen_candidates = {}  # allergen -> list of potential ingredients
for a, foods_with_alg in allergen_foods.items():
    #print(a, foods)
    all_allergens.append(a)

    candidates = set()
    for i, f in enumerate(foods_with_alg):
        if i == 0:
            candidates = set(foods[f])
        else:
            candidates = candidates.intersection(foods[f])

    allergen_candidates[a] = candidates
    print(a, candidates)

#for i, foods in ing_foods.items():
#    print(i, foods)

all_ing_map = {}
res = None

def search(cur):
    global res
    if cur == len(all_allergens):
        res = dict(all_ing_map)
        return True
    for ing in allergen_candidates[all_allergens[cur]]:
        if ing in all_ing_map.values():
            continue
        all_ing_map[all_allergens[cur]] = ing
        search(cur+1)
        all_ing_map[all_allergens[cur]] = None


search(0)

print(res)
print()

cnt = 0
for f in foods:
    for ing in f:
        if ing not in res.values():
            cnt += 1

print(cnt)

res = [i for a,i in sorted((a,i) for a,i in res.items())]
print(','.join(res))
