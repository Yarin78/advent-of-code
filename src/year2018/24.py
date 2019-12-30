import sys
import re

immune = []
infection = []


class Group:

    def __init__(self, army, group, no_units, hp, attack, attack_type, initiative, weaknesses, immunities):
        self.army = army
        self.group = group
        self.no_units=no_units
        self.hp=hp
        self.attack=attack
        self.attack_type=attack_type
        self.initiative=initiative
        self.weaknesses=weaknesses
        self.immunities=immunities

    def __str__(self):
        return 'Group %d has %d units with hp %d, attack %d, attack_type %s, initiative %d, weaknesses %s, immunities %s' % (self.group, self.no_units, self.hp, self.attack, self.attack_type, self.initiative, str(self.weaknesses), str(self.immunities))

    def effective_power(self):
        return self.no_units * self.attack

    def damage_potential(self, g):
        damage = self.attack
        if self.attack_type in g.weaknesses:
            damage *= 2
        if self.attack_type in g.immunities:
            damage = 0
        return self.no_units * damage


def parse_group(s, army, group_no):
    #4081 units each with 8009 hit points (immune to slashing, radiation; weak to bludgeoning, cold) with an attack that does 17 fire damage at initiative 7
    p=re.compile("([0-9]+) units each with ([0-9]+) hit points (.*)with an attack that does ([0-9]+) ([a-z]+) damage at initiative ([0-9]+)")
    m=p.search(s)
    if not m:
        print 'oops %s' % s
        exit(1)
    params = list(m.groups())
    weaknesses = []
    immunities = []
    if params[2]:
        for part in params[2].split(';'):
            if 'weak to' in part:
                a = weaknesses
                q = part[part.index('weak to') + 8:]
            else:
                a = immunities
                q = part[part.index('immune to') + 10:]
            q=q.replace(')', ' ').replace(',', ' ')

            for qq in q.split(' '):
                if qq:
                    a.append(qq)
        #print immunities
    return Group(army, group_no, int(params[0]), int(params[1]), int(params[3]), params[4], int(params[5]), weaknesses, immunities)


#immune.append(Group('immune', 1, 17, 5390, 4507, 'fire', 2, ['radiation', 'bludgeoning'], []))
#immune.append(Group('immune', 2, 989, 1274, 25, 'slashing', 3, ['bludgeoning', 'slashing'], ['fire']))

#infection.append(Group('infection', 1, 801, 4706, 116, 'bludgeoning', 1, ['radiation'], []))
#infection.append(Group('infection', 2, 4485, 2961, 12, 'slashing', 4, ['fire', 'cold'], ['radiation']))

immune_boost = 61 # 61

for line in sys.stdin.readlines():
    line = line.strip()
    if not line:
        continue
    if line.endswith(':'):
        line = line[:-1]
        army = line.split(' ')[0].lower()
        continue
    a = immune if army == 'immune' else infection
    g = parse_group(line, army, len(a) + 1)
    a.append(g)
    if army == 'immune':
        g.attack += immune_boost
    #print g


def enemy(army):
    global immune, infection
    return infection if army == 'immune' else immune




rounds = 0
while len(immune) > 0 and len(infection) > 0:
    rounds += 1
    print 'Round %d' % rounds
    print 'Immune'
    for g in immune:
        print 'Group %d contains %d units' % (g.group, g.no_units)
    print 'Infection'
    for g in infection:
        print 'Group %d contains %d units' % (g.group, g.no_units)
    print

    # Target selection

    ep = []
    all = immune + infection
    all.sort(cmp=lambda x,y: y.effective_power() - x.effective_power() if y.effective_power () != x.effective_power() else y.initiative - x.initiative)

    being_attacked = []
    attacks = []

    for g in all:
        most_dmg = 0
        most_ep = 0
        most_initiative = 0
        target = None
        for ge in enemy(g.army):
            if ge in being_attacked:
                continue
            #print '%s group %s would deal defending group %d %d damage' % (g.army, g.group, ge.group, g.damage_potential(ge))
            if g.damage_potential(ge) > most_dmg or (g.damage_potential(ge) == most_dmg and ge.effective_power() > most_ep) or (g.damage_potential(ge) == most_dmg and ge.effective_power() == most_ep and ge.initiative > most_initiative):
                target = ge
                most_dmg = g.damage_potential(ge)
                most_ep = ge.effective_power()
                most_initiative = ge.initiative

        if target and most_dmg > 0:
            being_attacked.append(target)
            attacks.append((g, target, most_dmg))

            print '  %s group %d chooses %s group %d' % (g.army, g.group, target.army, target.group)

    attacks.sort(cmp=lambda x,y: y[0].initiative-x[0].initiative)
    print

    for (attacker, defender, damage) in attacks:
        if attacker.no_units <= 0:
            continue

        damage = attacker.damage_potential(defender)
        units_lost = damage / defender.hp
        if defender.no_units < units_lost:
            units_lost = defender.no_units
        print '%s group %d attackas %s group %d dealing %d damage, killing %d units' % (attacker.army, attacker.group, defender.army, defender.group, damage, units_lost)
        defender.no_units -= units_lost

    print

    immune = [x for x in immune if x.no_units > 0]
    infection = [x for x in infection if x.no_units > 0]

    #if rounds == 2:
    #    break


units_left = 0
print 'Immune'
for g in immune:
    print 'Group %d contains %d units' % (g.group, g.no_units)
    units_left += g.no_units
print 'Infection'
for g in infection:
    print 'Group %d contains %d units' % (g.group, g.no_units)
    units_left += g.no_units
print
print 'Units left', units_left
