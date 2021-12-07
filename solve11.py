#!/bin/env python
from aocd import get_data, submit


def main():
    values = [int(x) for x in get_data(day=11, year=2021).split(",")]
    testvalues = [int(x) for x in "16,1,2,0,4,2,7,1,2,14".split(",")]
    testtrue = 0
    testtrue2 = 0

    testresult = solve11(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve11(values)
    print("solve11:", result)

    # input("submit?")
    submit(result, part="a", day=11, year=2021)

    testresult2 = solve11_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve11_2(values)
    print("solve11_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=11, year=2021)


def solve11(values):
    ...


def solve11_2(values):
    ...


if __name__ == "__main__":
    main()
