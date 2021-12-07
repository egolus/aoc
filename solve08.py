#!/bin/env python
from aocd import get_data, submit


def main():
    values = [int(x) for x in get_data(day=8, year=2021).split(",")]
    testvalues = [int(x) for x in "16,1,2,0,4,2,7,1,2,14".split(",")]
    testtrue = 0
    testtrue2 = 0

    testresult = solve08(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve08(values)
    print("solve08:", result)

    # input("submit?")
    submit(result, part="a", day=8, year=2021)

    testresult2 = solve08_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve08_2(values)
    print("solve08_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=8, year=2021)


def solve08(values):
    ...


def solve08_2(values):
    ...


if __name__ == "__main__":
    main()
