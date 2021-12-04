#!/bin/env python

with open("../input01", "r") as infile:
    lines = list(int(x) for x in infile.readlines())


def solve01():
    ilines = iter(lines)
    counterIncreased = -1
    old = 0
    for line in ilines:
        if line > old:
            counterIncreased += 1
        old = line
    return counterIncreased


def solve01_2():
    s0 = lines[0]
    s1 = lines[1]
    triCounter = -1
    old = 0

    for line in lines[2:]:
        s = sum([s0, s1, line])
        if s > old:
            triCounter += 1
        old, s0, s1 = (s, s1, line)

    return triCounter


if __name__ == "__main__":
    print("solve01:", solve01())
    print("solve01_2:", solve01_2())
