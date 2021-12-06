#!/bin/env python
from aocd import get_data, submit


def main():
    lines = get_data(day=7, year=2021)
    testlines = [""]
    assert solve07(testlines) == 0
    result = solve07(lines)
    print("solve07:", result)
    submit(result, part="a", day=7, year=2021)
    assert solve07_2(testlines) == 0
    result2 = solve07_2(lines)
    print("solve07_2:", result2)
    submit(result2, part="b", day=7, year=2021)


def solve07(lines):
    ...


def solve07_2(lines):
    ...


if __name__ == "__main__":
    main()
