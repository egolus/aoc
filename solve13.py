#!/bin/env python
from aocd import get_data, submit
from pprint import pprint


def main():
    values = get_data(day=13, year=2021).split("\n")
    testvalues = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".split("\n")
    testtrue = 17
    testtrue_b = "O"

    testresult = solve13(testvalues, debug=True)
    assert testresult == testtrue, f"{testresult} != {testtrue}"

    result = solve13(values)
    print("solve13:", result)

    # input("submit?")
    submit(result, part="a", day=13, year=2021)

    testresult_b = solve13_b(testvalues, debug=True)
    assert testresult_b == testtrue_b, f"{testresult_b} != {testtrue_b}"

    result_b = solve13_b(values)
    print("solve13_b:", result_b)

    # input("submit?")
    submit(result_b, part="b", day=13, year=2021)


def solve13(lines, debug=False):
    splitter = lines.index("")
    dots = [(int(line.split(",")[0]), int(line.split(",")[1]))
            for line in lines[:splitter]]
    if debug:
        maxX = max([x for x, _ in dots])
        maxY = max([y for _, y in dots])
    folds = [(line.split(" ")[2].split("=")[0],
              int(line.split(" ")[2].split("=")[1]))
             for line in lines[splitter + 1:]]
    if debug:
        print("dots:", dots)
        print("folds:", folds)
        printDots(dots, maxX, maxY)
    for fold in folds:
        if debug:
            print(fold)
        dots = doFold(dots, fold)
        if debug:
            maxX = max([x for x, _ in dots])
            maxY = max([y for _, y in dots])
            printDots(dots, maxX, maxY)
        return len(dots)


def doFold(dots, fold):
    axis = 0 if fold[0] == "x" else 1
    for i in range(len(dots)):
        if dots[i][axis] > fold[1]:
            if axis == 0:
                dots[i] = (fold[1] - (dots[i][axis] - fold[1]), dots[i][1])
            else:
                dots[i] = (dots[i][0], fold[1] - (dots[i][axis] - fold[1]))
    return list(set(dots))


def printDots(dots, maxX, maxY):
    for y in range(maxY + 1):
        for x in range(maxX + 1):
            print("#" if ((x, y) in dots) else ".", end="")
        print()


def solve13_b(lines, debug=False):
    splitter = lines.index("")
    dots = [(int(line.split(",")[0]), int(line.split(",")[1]))
            for line in lines[:splitter]]
    if debug:
        maxX = max([x for x, _ in dots])
        maxY = max([y for _, y in dots])
    folds = [(line.split(" ")[2].split("=")[0],
              int(line.split(" ")[2].split("=")[1]))
             for line in lines[splitter + 1:]]
    if debug:
        print("dots:", dots)
        print("folds:", folds)
        printDots(dots, maxX, maxY)
    for fold in folds:
        if debug:
            print(fold)
        dots = doFold(dots, fold)
        if debug:
            maxX = max([x for x, _ in dots])
            maxY = max([y for _, y in dots])
            printDots(dots, maxX, maxY)
    dots = sorted(dots)
    maxX = max([x for x, _ in dots])
    maxY = max([y for _, y in dots])
    printDots(dots, maxX, maxY)
    pprint(dots)
    return charRecognition(dots, maxX)


def charRecognition(dots, maxX):
    chars = {
        "E": [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 0),
            (2, 0),
            (2, 1),
            (2, 2),
            (3, 0),
            (4, 0),
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3),
        ],
        "G": [
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 3),
            (2, 0),
            (3, 0),
            (3, 2),
            (3, 3),
            (4, 0),
            (4, 3),
            (5, 1),
            (5, 2),
            (5, 3),
        ],
        "L": [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3),
        ],
        "O": [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 0),
            (1, 4),
            (2, 0),
            (2, 4),
            (3, 0),
            (3, 4),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 4),
        ],
        "R": [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 3),
            (2, 0),
            (2, 3),
            (3, 0),
            (3, 1),
            (3, 2),
            (4, 0),
            (4, 2),
            (5, 3),
        ],
        "P": [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 3),
            (2, 0),
            (2, 3),
            (3, 0),
            (3, 1),
            (3, 2),
            (4, 0),
            (4, 0),
            (5, 0),
            (5, 0),
        ],
        "U": [
            (0, 0),
            (0, 3),
            (1, 0),
            (1, 3),
            (2, 0),
            (2, 3),
            (3, 0),
            (3, 3),
            (4, 0),
            (4, 3),
            (5, 1),
            (5, 2),
        ]
    }
    ret = ""
    offset = 0
    while offset < maxX:
        for name, char in chars.items():
            print("trying", name)
            for cdot in char:
                if (cdot[1] + offset, cdot[0]) not in dots:
                    print(f"pixel ({cdot[0] + offset}, {cdot[1]}) wrong")
                    break
            else:
                ret += name
                break
        offset += 5
    return ret


if __name__ == "__main__":
    main()
