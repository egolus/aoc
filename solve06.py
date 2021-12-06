#!/bin/env python
from aocd import lines, submit

with open("../input06", "r") as infile:
    lines = list(x.strip() for x in infile.readlines())
    testlines = ["3,4,3,1,2"]
    fishesIn = [int(x) for x in lines[0].split(",")]
    # fishesIn = [int(x) for x in testlines[0].split(",")]
    days = []
    days2 = []


def solve06(fishes):
    for day in range(80):
        for i in range(len(fishes)):
            fishes[i] -= 1
            if fishes[i] <= -1:
                fishes[i] = 6
                fishes.append(8)
        days.append({
            x: fishes.count(x) for x in range(8)
        })

    return len(fishes)


def solve06_2(fishes):
    dayrange = 256
    result = 0
    fishtimes = {}
    for i in range(8):
        fishtimes[i] = len([x for x in fishes if x == i])

    for i in range(dayrange):
        fishtimes[(i - 1) % 8] += fishtimes[i % 8]  # reset to 6
        fishtimes[((i + 1) % 8) + 8] = fishtimes[i % 8]  # add new with 8
        fishtimes[i % 8] = fishtimes.pop((i % 8) + 8, 0)  # get fishes of next week
        days2.append(dict(x for x in fishtimes.items()))
    for i in fishtimes.values():
        result += i
    return result


if __name__ == "__main__":
    result = solve06(fishesIn.copy())
    print("solve06:", result)
    submit(result, part="a", day=6, year=2021)
    result2 = solve06_2(fishesIn.copy())
    print("solve06_2:", result2)
    submit(result2, part="b", day=6, year=2021)
