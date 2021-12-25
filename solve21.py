#!/bin/env python
from aocd import get_data, submit


def main():
    values = get_data(day=21, year=2021)
    testvalues = """Player 1 starting position: 4
Player 2 starting position: 8"""
    testtrue = 739785
    testtrue2 = 444356092776315

    testresult = solve21(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve21(values)
    print("solve21:", result)

    # input("submit?")
    submit(result, part="a", day=21, year=2021)

    testresult2 = solve21_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve21_2(values)
    print("solve21_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=21, year=2021)


def solve21(values):
    p1, p2 = [{"pos": int(line.split(": ")[1]), "count": 0} for line in values.splitlines()]
    counter = -1
    rolls = 0
    while p1["count"] < 1000 and p2["count"] < 1000:
        print(p1, p2, counter, rolls)
        for p in (p1, p2):
            rolls += 3
            p["pos"] = ((p["pos"] + 3 * (counter + 3) -1) % 10) + 1
            p["count"] += p["pos"]
            if p["count"] >= 1000:
                break
            counter = (counter + 3) % 100
    print(p1, p2, counter, rolls)
    return (p1["count"] if p1["count"] < p2["count"] else p2["count"]) * rolls


def solve21_2(values):
    ...


if __name__ == "__main__":
    main()
