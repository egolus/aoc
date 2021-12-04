#!/bin/env python
with open("../input04", "r") as infile:
    lines = list(x.strip() for x in infile.readlines())


def readBoards():
    board = {}
    index = 0
    for line in lines[1:]:
        if line != "":
            board[index] = [int(x) for x in line.split(" ") if x]
            index += 1
        else:
            if board:
                yield board
                board = {}
                index = 0


def printBoard(board):
    for line in board.values():
        print(" ".join(f"{nu:>2}" for nu in line))
    print()


def solve04():
    bingo = [int(x) for x in lines[0].split(",")]

    boards = [board for board in readBoards()]

    for num in bingo:
        print(f"number: {num}\n")
        found = False
        for board in boards:
            for line in board.values():
                for i in range(len(line)):
                    if line[i] == num:
                        line[i] = "X"
                if set(line) == {"X"}:
                    print("BINGO")
                    found = True
                    break
            for i in range(len(list(board.values())[0])):
                col = [line[i] for line in board.values()]
                if set(col) == {"X"}:
                    print("BINGO")
                    found = True
                    break
            printBoard(board)
            if found:
                break
        if found:
            nums = 0
            for line in board.values():
                for i in line:
                    if i != "X":
                        nums += i
                        print(f"{i:>3}", end="")
            print("\n", nums)
            return nums * num


def solve04_2():
    bingo = [int(x) for x in lines[0].split(",")]

    boards = [board for board in readBoards()]

    for num in bingo:
        print(f"number: {num}, boards: {len(boards)}\n")
        for bi in range(len(boards)-1, 0, -1):
            print(f"bi: {bi}")
            board = boards[bi]
            found = False
            for line in board.values():
                for i in range(len(line)):
                    if line[i] == num:
                        line[i] = "X"
                if set(line) == {"X"}:
                    print("BINGO")
                    found = True
                    break
            for i in range(len(list(board.values())[0])):
                col = [line[i] for line in board.values()]
                if set(col) == {"X"}:
                    print("BINGO")
                    found = True
                    break
            printBoard(board)
            if found:
                boards.pop(bi)
            print(len(boards))
        if len(boards) <= 1:
            nums = 0
            for line in board.values():
                for i in line:
                    if i != "X":
                        nums += i
                        print(f"{i:>3}", end="")
            print("\n", nums)
            return nums * num


if __name__ == "__main__":
    print("solve04:", solve04())
    print("solve04_2:", solve04_2())
