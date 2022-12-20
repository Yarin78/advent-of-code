import sys

sequence = [int(line) for line in sys.stdin.readlines()]
n = len(sequence)

def mix_it(seq, mix_order):
    for (i, x) in mix_order:
        pos = seq.index((i,x))
        new_pos = (pos + x) % (n-1)
        seq = seq[:pos] + seq[pos+1:]
        seq = seq[:new_pos] + [(i,x)] + seq[new_pos:]
    return seq

def score(sequence):
    values = [p[1] for p in sequence]
    zero_pos = values.index(0)

    return (values[(zero_pos + 1000)%n] +
        values[(zero_pos + 2000)%n] +
        values[(zero_pos + 3000)%n])



part1_seq = [(i, x) for i,x in enumerate(sequence)]
mix_order = part1_seq[:]
print(score(mix_it(part1_seq, mix_order)))

part2_seq = [(i, x * 811589153) for i,x in enumerate(sequence)]
mix_order = part2_seq[:]
for _ in range(10):
    part2_seq = mix_it(part2_seq, mix_order)
print(score(part2_seq))
