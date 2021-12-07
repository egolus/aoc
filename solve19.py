#!/bin/env python
from aocd import get_data, submit


def main():
    values = [int(x) for x in get_data(day=19, year=2021).split(",")]
    testvalues = [int(x) for x in "16,1,2,0,4,2,7,1,2,14".split(",")]
    testtrue = 0
    testtrue2 = 0

    testresult = solve19(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve19(values)
    print("solve19:", result)

    # input("submit?")
    submit(result, part="a", day=19, year=2021)

    testresult2 = solve19_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve19_2(values)
    print("solve19_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=19, year=2021)


def solve19(values):
    ...


def solve19_2(values):
    ...


if __name__ == "__main__":
    main()
