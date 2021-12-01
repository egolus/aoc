#!/bin/env python

with open("../input01", "r") as infile:
    lines = list(int(x) for x in infile.readlines())

ilines = iter(lines)
counterIncreased = -1
old = 0
for line in ilines:
    if line > old:
        counterIncreased += 1
    old = line

print()
print(f"final counterIncreased: {counterIncreased}")


s0 = lines[0]
s1 = lines[1]
triCounter = -1
old = 0

for line in lines[2:]:
    s = sum([s0, s1, line])
    if s > old:
        triCounter += 1
    old, s0, s1 = (s, s1, line)

print()
print(f"final triCounter: {triCounter}")

