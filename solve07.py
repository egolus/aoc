#!/bin/env python
from aocd import get_data, submit


def main():
    lines = [int(x) for x in get_data(day=7, year=2021).split(",")]
    testlines = [int(x) for x in "16,1,2,0,4,2,7,1,2,14".split(",")]
    testresult = solve07(testlines)
    assert testresult == 37, f"{testresult} != 37"
    result = solve07(lines)
    print("solve07:", result)
    submit(result, part="a", day=7, year=2021)
    testresult2 = solve07_2(testlines)
    assert testresult2 == 168, f"{testresult2} != 168"
    result2 = solve07_2(lines)
    print("solve07_2:", result2)
    submit(result2, part="b", day=7, year=2021)


def solve07(positions):
    result = 0
    for target in range(max(positions)):
        res = 0
        for position in positions:
            res += abs(position - target)
        if result == 0 or res <= result:
            result = res
    return result


def solve07_2(positions):
    result = 0
    for target in range(max(positions)):
        res = 0
        for position in positions:
            n = abs(position - target)
            res += ((n * (n + 1)) // 2)
        if result == 0 or res <= result:
            result = res
    return result


if __name__ == "__main__":
    main()
