#!/bin/env python
import itertools
from aocd import get_data, submit


def main():
    values = get_data(day=25, year=2021)
    testvalues = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
    testtrue = 58
    testtrue2 = 0

    testresult = solve24(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve24(values)
    print("solve25:", result)

    # input("submit?")
    submit(result, part="a", day=25, year=2021)

    testresult2 = solve24_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve24_2(values)
    print("solve25_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=25, year=2021)


def printBoard(board):
    for line in board:
        for c in line:
            print(c, end="")
        print()
    print()


def solve24(values, maxSteps=None):
    board = []
    for line in values.splitlines():
        board.append([c for c in line])
    w, h = len(board[0]), len(board)
    changed = True
    step = 0

    print("initial:")
    printBoard(board)

    while changed:
        step += 1
        print("step:", step)
        changed = False
        newboard = []
        for line in board:
            newLine = [c for c in line]
            for i in range(len(newLine)):
                if line[i] == "." and line[(i-1) % w] == ">":
                    newLine[i] = ">"
                    newLine[(i-1) % w] = "."
                    changed = True
            newboard.append(newLine)
        board = [[c for c in line] for line in newboard]
        for i in range(h):
            for j in range(w):
                if board[i][j] == "." and board[(i-1) % h][j] == "v":
                    newboard[i][j] = "v"
                    newboard[(i-1) % h][j] = "."
                    changed = True
        board = [[c for c in line] for line in newboard]
        printBoard(board)
        if (maxSteps and step >= maxSteps):
            break
    return step


def solve24_2(values):
    ...


if __name__ == "__main__":
    main()
