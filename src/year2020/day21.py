import sys
from collections import defaultdict
from yal.matching import bipartite_matching

foods = []  # row number -> list of ingredients
allergen_foods = defaultdict(list)  # allergen -> list of row numbers containing the allergen
for line_num, line in enumerate(line.strip() for line in sys.stdin.readlines()):
    (ing_list, all_list) = line.split(' (contains ')
    foods.append(ing_list.split(' '))
    for a in all_list[:-1].split(', '):
        allergen_foods[a].append(set(ing_list.split(' ')))

res = bipartite_matching({a: set.intersection(*foods_with_alg) for a, foods_with_alg in allergen_foods.items()})

print(sum(ing not in res.values() for f in foods for ing in f))
print(','.join([i for a,i in sorted((a,i) for a,i in res.items())]))
