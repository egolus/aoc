#!/bin/env python

with open("../input05", "r") as infile:
    lines = list(x.strip() for x in infile.readlines())
    # lines = """0,9 -> 5,9
# 8,0 -> 0,8
# 9,4 -> 3,4
# 2,2 -> 2,1
# 7,0 -> 7,4
# 6,4 -> 2,0
# 0,9 -> 2,9
# 3,4 -> 1,4
# 0,0 -> 8,8
# 5,5 -> 8,2""".split("\n")

    vents = []
    boardSizes = [0, 0]
    for line in lines:
        splits = line.split(" ")
        vent = {
            "x1": int(splits[0].split(",")[0]),
            "y1": int(splits[0].split(",")[1]),
            "x2": int(splits[2].split(",")[0]),
            "y2": int(splits[2].split(",")[1]),
        }
        vents.append(vent)
        if vent["x1"] > boardSizes[0]:
            boardSizes[0] = vent["x1"]
        if vent["x2"] > boardSizes[0]:
            boardSizes[0] = vent["x2"]
        if vent["y1"] > boardSizes[1]:
            boardSizes[1] = vent["y1"]
        if vent["y2"] > boardSizes[1]:
            boardSizes[1] = vent["y2"]
    board = [
        list(0 for _ in range(boardSizes[0] + 1))
        for _ in range(boardSizes[1] + 1)
    ]


def solve05():
    for vent in vents:
        if vent["x1"] != vent["x2"] and vent["y1"] != vent["y2"]:
            print(f"diag {vent['x1']},{vent['y1']} {vent['x2']},{vent['y2']}")
            yPos = True
            xPos = True
            if vent["y1"] > vent["y2"]:
                yPos = False
            if vent["x1"] > vent["x2"]:
                xPos = False
            x = vent["x1"]
            y = vent["y1"]
            while True:
                board[y][x] += 1
                if y != vent["y2"]:
                    y += 1 if yPos else -1
                else:
                    break
                if x != vent["x2"]:
                    x += 1 if xPos else -1
                else:
                    break
            continue

        try:
            if vent["x1"] < vent["x2"]:
                print(f" x1 -> x2 {vent['x1']} {vent['x2']}")
                for x in range(vent["x1"], vent["x2"] + 1):
                    board[vent["y1"]][x] += 1
            elif vent["x1"] > vent["x2"]:
                print(f" x2 -> x1 {vent['x1']} {vent['x2']}")
                for x in range(vent["x2"], vent["x1"] + 1):
                    board[vent["y1"]][x] += 1
            elif vent["y1"] < vent["y2"]:
                print(f" y1 -> y2 {vent['y1']} {vent['y2']}")
                for y in range(vent["y1"], vent["y2"] + 1):
                    board[y][vent["x1"]] += 1
            elif vent["y1"] > vent["y2"]:
                print(f" y2 -> y1 {vent['y1']} {vent['y2']}")
                for y in range(vent["y2"], vent["y1"] + 1):
                    board[y][vent["x1"]] += 1
            else:
                print(f" x=x y=y")
                if vent["y1"] == vent["y2"]:
                    board[vent["y1"]]["x1"] += 1
        except Exception:
            print(vent, boardSizes)
    count = 0
    for line in board:
        for i in line:
            if i > 1:
                count += 1

    for y in range(len(board)):
        print("".join(str(i) for i in board[y]))
    return count


def solve05_2():
    ...


if __name__ == "__main__":
    print("solve05:", solve05())
    print("solve05_2:", solve05_2())
