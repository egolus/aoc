#!/bin/env python
import sys
from aocd import get_data, submit


def main():
    values = get_data(day=15, year=2021).split("\n")
    testvalues = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".split("\n")
    testtrue = 40
    testtrue2 = 315

    testresult = solve15(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve15(values)
    print("solve15:", result)

    # input("submit?")
    submit(result, part="a", day=15, year=2021)

    testresult2 = solve15_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve15_2(values)
    print("solve15_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=15, year=2021)


def buildMap(values, repeatX=0, repeatY=0):
    maxX = len(values[0])
    maxY = len(values)
    start = (0, 0)
    risks = {}
    for ry in range(repeatY + 1):
        for y in range(len(values)):
            for rx in range(repeatX + 1):
                for x in range(len(values[0])):
                    val = (int(values[y][x]) + rx + ry)
                    if val > 9:
                        val = (val % 9)
                    risks[((x + (maxX * rx)), (y + (maxY * ry)))] = val
    risks[start] = 0
    return (risks, maxX * (repeatX + 1), maxY * (repeatY + 1))


def printMap(risks, maxX, maxY, path=None):
    if path is None:
        path = {}
    print(" ", "0123456789 " * (maxX // 10))
    print()
    for y in range(maxY):
        print(y % 10, end=" ")
        for x in range(maxX):
            if (x, y) in path or (x, y) == (maxX, maxY):
                print("_", end="")
            else:
                print(risks.get((x, y), "."), end="")
            if (x % 10 == 9) and x > 0:
                print(" ", end="")
        if (y % 10 == 9) and y > 0:
            print("\n", end="")
        print()
    print()
    print()


def aStar(risks):
    maxX = max(risks.keys())[0]
    maxY = max(risks.keys())[1]
    start = (0, 0)
    goal = (maxX, maxY)
    openSet = {start}
    cameFrom = {}
    gScore = {}
    gScore[start] = 0
    fScore = {}
    fScore[start] = 0
    # print(f"risks: {risks}\nopenSet: {openSet}\ncameFrom: {cameFrom}\ngScore: {gScore}\nfScore: {fScore}")

    while openSet:
        current = min(openSet, key=lambda a: fScore.get(a, sys.maxsize))
        # if current == goal:
            # # print(f"risks: {risks}\nopenSet: {openSet}\ncameFrom: {cameFrom}\ngScore: {gScore}\nfScore: {fScore}")
            # return (reconstructPath(cameFrom, current), fScore[current])

        openSet.remove(current)
        for neighbor in getNeighbors(current, maxX, maxY):
            tentativeGScore = gScore[current] + risks[neighbor]
            if (neighbor not in gScore) or (tentativeGScore < gScore[neighbor]):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentativeGScore
                fScore[neighbor] = tentativeGScore
                openSet.add(neighbor)
        # print(f"risks: {risks}\nopenSet: {openSet}\ncameFrom: {cameFrom}\ngScore: {gScore}\nfScore: {fScore}")
    return (reconstructPath(cameFrom, goal, risks), fScore[goal])


def getNeighbors(node, maxX, maxY):
    neighbors = []
    if node[0] > 0:
        neighbors.append((node[0] - 1, node[1]))
    if node[0] < maxX:
        neighbors.append((node[0] + 1, node[1]))
    if node[1] > 0:
        neighbors.append((node[0], node[1] - 1))
    if node[1] < maxY:
        neighbors.append((node[0], node[1] + 1))
    return neighbors


def reconstructPath(cameFrom, current, risks):
    path = [current]
    pathSum = 0
    while current in cameFrom.keys():
        current = cameFrom[current]
        pathSum += risks[current]
        path = [current] + path
    print(pathSum)
    return path


def solve15(values):
    risks, maxX, maxY = buildMap(values)
    path, risk = aStar(risks)
    print("final path:", path)
    printMap(risks, maxX, maxY, path)
    return risk


def solve15_2(values):
    risks, maxX, maxY = buildMap(values, 4, 4)
    path, risk = aStar(risks)
    print("final path:", path)
    printMap(risks, maxX, maxY, path)
    return risk


if __name__ == "__main__":
    main()
