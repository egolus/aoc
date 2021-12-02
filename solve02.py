#!/bin/env python

with open("../input02", "r") as infile:
    lines = list(x.strip() for x in infile.readlines())


def solve02():
    position = [0, 0]
    for line in lines:
        move, X = line.split(" ")
        if move == "forward":
            position[0] += int(X)
        elif move == "down":
            position[1] += int(X)
        elif move == "up":
            position[1] -= int(X)
    return position[0] * position[1]


def solve02_2():
    position = [0, 0]
    aim = 0
    for line in lines:
        move, X = line.split(" ")
        if move == "down":
            aim += int(X)
        elif move == "up":
            aim -= int(X)
        elif move == "forward":
            position[0] += int(X)
            position[1] += int(X) * aim
    return position[0] * position[1]


if __name__ == "__main__":
    print("solve02:", solve02())
    print("solve02_2:", solve02_2())
