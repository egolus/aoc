#!/bin/env python
from itertools import count
from aocd import get_data, submit


def main():
    values = get_data(day=11, year=2021).split("\n")
    testvalues0 = """11111
19991
19191
19991
11111""".split("\n")
    testvalues1 = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".split("\n")
    testtrue0 = 9
    testtrue1 = 204
    testtrue1_1 = 1656
    testtrue2 = 195

    testresult0 = solve11(testvalues0, 2)
    assert testresult0 == testtrue0, f"{testresult0} != {testtrue0}"

    testresult1 = solve11(testvalues1, 10)
    assert testresult1 == testtrue1, f"{testresult1} != {testtrue1}"

    testresult1_1 = solve11(testvalues1, 100)
    assert testresult1 == testtrue1, f"{testresult1_1} != {testtrue1_1}"
    result = solve11(values, 100)
    print("solve11:", result)

    # input("submit?")
    submit(result, part="a", day=11, year=2021)

    testresult2 = solve11_2(testvalues1)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve11_2(values)
    print("solve11_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=11, year=2021)


class Solver():
    lines = None
    height = 0
    width = 0
    flashes = 0

    def __init__(self, values):
        self.height = len(values)
        self.width = len(values[0])
        self.lines = []
        for line in values:
            self.lines.append([int(x) for x in line])

    def iter(self):
        for y in range(self.height):
            for x in range(self.width):
                self.lines[y][x] += 1
                if self.lines[y][x] == 10:
                    self.flashAdjacent(x, y)
        for y in range(self.height):
            for x in range(self.width):
                if self.lines[y][x] >= 10:
                    self.flashes += 1
                    self.lines[y][x] = 0

        for line in self.lines:
            for it in line:
                if it > 0:
                    return False
        return True

    def flashAdjacent(self, x, y):
        xl = x if x == 0 else x - 1
        xh = x if x == self.width - 1 else x + 1
        yl = y if y == 0 else y - 1
        yh = y if y == self.height - 1 else y + 1
        for ny in range(yl, yh + 1):
            for nx in range(xl, xh + 1):
                self.lines[ny][nx] += 1
                if self.lines[ny][nx] == 10:
                    self.flashAdjacent(nx, ny)

    def print(self):
        for line in self.lines:
            for it in line:
                print(f"{it:>2}", end=" ")
            print()
        print()


def solve11(values, steps):
    solver = Solver(values)
    for step in range(steps):
        solver.iter()
    return solver.flashes


def solve11_2(values):
    solver = Solver(values)
    for step in count():
        if solver.iter() is True:
            return step + 1


if __name__ == "__main__":
    main()
