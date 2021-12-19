#!/bin/env python
from sys import maxsize
from itertools import count
from aocd import get_data, submit


def main():
    values = get_data(day=17, year=2021)
    testvalues = """target area: x=20..30, y=-10..-5"""
    testtrue = 45
    testtrue2 = 112

    testresult = solve17(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve17(values)
    print("solve17:", result)

    # input("submit?")
    submit(result, part="a", day=17, year=2021)

    testresult2 = solve17_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve17_2(values)
    print("solve17_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=17, year=2021)


def solve17(data):
    result = 0
    target = {}
    _, _, x, y = data.split(" ")
    x = x.split("=")[1].strip()[:-1]
    target["xl"] = int(x.split("..")[0])
    target["xh"] = int(x.split("..")[1])
    y = y.split("=")[1].strip()
    target["yl"] = int(y.split("..")[0])
    target["yh"] = int(y.split("..")[1])
    print("target:", target)
    print()

    for x in range(1, target["xl"] + 1):
        for y in range(1, - target["yl"]):
            initial = {"x": x, "y": y}
            if not y % 1000:
                print("shot:", initial, ", current highest:", result)
            position = {"x": 0, "y": 0}
            highest = 0

            velocity = {"x": initial["x"], "y": initial["y"]}
            for step in range(1000):
                position, velocity = updatePosition(position, velocity)
                highest = max(position["y"], highest)

                if ((target["xl"] <= position["x"] <= target["xh"]) and
                        (target["yl"] <= position["y"] <= target["yh"])):
                    # hit target
                    print("shot:", initial, " - hit",
                          f"new high: {highest}" if highest > result else "")
                    if highest > result:
                        result = highest
                elif (position["x"] > target["xh"]):
                    # overshot target
                    break
        else:
            continue
        break
    return result


def updatePosition(position, velocity):
    position = {"x": position["x"] + velocity["x"], "y": position["y"] + velocity["y"]}
    newVelocity = {"x": velocity["x"], "y": velocity["y"]}
    if newVelocity["x"] > 0:
        newVelocity["x"] -= 1
    elif newVelocity["x"] < 0:
        newVelocity["x"] += 1
    newVelocity["y"] -= 1
    return (position, newVelocity)


def solve17_2(data):
    result = 0
    target = {}
    _, _, x, y = data.split(" ")
    x = x.split("=")[1].strip()[:-1]
    target["xl"] = int(x.split("..")[0])
    target["xh"] = int(x.split("..")[1])
    y = y.split("=")[1].strip()
    target["yl"] = int(y.split("..")[0])
    target["yh"] = int(y.split("..")[1])
    print("target:", target)
    print()

    for x in range(1, target["xh"] + 1):
        for y in range(target["yl"], - target["yl"]):
            initial = {"x": x, "y": y}
            position = {"x": 0, "y": 0}

            velocity = {"x": initial["x"], "y": initial["y"]}
            for step in range(1000):
                position, velocity = updatePosition(position, velocity)

                if ((target["xl"] <= position["x"] <= target["xh"]) and
                        (target["yl"] <= position["y"] <= target["yh"])):
                    # hit target
                    print("shot:", initial, " - hit",)
                    result += 1
                    break
                elif (position["x"] > target["xh"]):
                    # overshot target
                    break
        else:
            continue
        break
    return result


if __name__ == "__main__":
    main()
