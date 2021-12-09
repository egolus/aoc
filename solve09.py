#!/bin/env python
from aocd import get_data, submit


def main():
    values = get_data(day=9, year=2021).split("\n")
    testvalues = """2199943210
3987894921
9856789892
8767896789
9899965678""".split("\n")
    testtrue = 15
    testtrue2 = 1134

    testresult = solve09(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve09(values)
    print("solve09:", result)

    # input("submit?")
    submit(result, part="a", day=9, year=2021)

    testresult2 = solve09_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve09_2(values)
    print("solve09_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=9, year=2021)


def solve09(values):
    """
    risk-level(low-point) = 1 + height
    -> 2, 1, 6, 6

    sum(risk-levels) = 2 + 1 + 6 + 6 = 15
    """
    print("values:", "\n".join(values), sep="\n")
    result = 0
    height = len(values)
    for i in range(height):
        width = len(values[0])
        for j in range(width):
            v = values[i][j]
            others = []
            if i == 0:
                others += [values[i + 1][j]]
            elif i == height - 1:
                others += [values[i - 1][j]]
            else:
                others += [values[i - 1][j], values[i + 1][j]]
            if j == 0:
                others += [values[i][j + 1]]
            elif j == width - 1:
                others += [values[i][j - 1]]
            else:
                others += [values[i][j - 1], values[i][j + 1]]
            if v < min(others):
                result += 1 + int(v)
    return result


def solve09_2(values):
    result = 1
    height = len(values)
    width = len(values[0])
    basins = []
    checkedValues = set()

    for i in range(height):
        for j in range(width):
            v = values[i][j]
            others = []
            if i == 0:
                others += [values[i + 1][j]]
            elif i == height - 1:
                others += [values[i - 1][j]]
            else:
                others += [values[i - 1][j], values[i + 1][j]]
            if j == 0:
                others += [values[i][j + 1]]
            elif j == width - 1:
                others += [values[i][j - 1]]
            else:
                others += [values[i][j - 1], values[i][j + 1]]
            if v < min(others):
                basins.append([(i, j)])
                checkedValues.add((i, j))
    for basin in basins:
        for point in basin:
            if point[0] > 0:
                other = (point[0] - 1, point[1])
                if other not in checkedValues:
                    if values[other[0]][other[1]] < "9":
                        basin.append(other)
                        checkedValues.add(other)
            if point[0] < height - 1:
                other = (point[0] + 1, point[1])
                if other not in checkedValues:
                    if values[other[0]][other[1]] < "9":
                        basin.append(other)
                        checkedValues.add(other)
            if point[1] > 0:
                other = (point[0], point[1] - 1)
                if other not in checkedValues:
                    if values[other[0]][other[1]] < "9":
                        basin.append(other)
                        checkedValues.add(other)
            if point[1] < width - 1:
                other = (point[0], point[1] + 1)
                if other not in checkedValues:
                    if values[other[0]][other[1]] < "9":
                        basin.append(other)
                        checkedValues.add(other)

    basinlengths = sorted(len(basin) for basin in basins)
    print(f"basinlengths: {basinlengths}")
    for i in basinlengths[-3:]:
        result = result * i
    return result


if __name__ == "__main__":
    main()
