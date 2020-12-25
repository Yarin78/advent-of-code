import sys

lines = [line.strip() for line in sys.stdin.readlines()]

card_key = int(lines[0])
door_key = int(lines[1])


cur = 1
card_loop_size = 0
while cur != card_key:
    card_loop_size += 1
    cur = (cur * 7) % 20201227

cur = 1
door_loop_size = 0
while cur != door_key:
    door_loop_size += 1
    cur = (cur * 7) % 20201227

print(card_loop_size, door_loop_size)

cur = 1
for i in range(card_loop_size):
    cur = (cur * door_key) % 20201227

print(cur)
