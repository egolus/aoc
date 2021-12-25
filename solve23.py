#!/bin/env python
from sys import maxsize
from bisect import insort_left
from aocd import get_data, submit
from pprint import pprint
import json


def main():
    values = get_data(day=23, year=2021)
    testvalues = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""
    testtrue = 12521
    testtrue2 = 0

    testresult = solve23(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve23(values)
    print("solve23:", result)

    # input("submit?")
    submit(result, part="a", day=23, year=2021)

    testresult2 = solve23_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve23_2(values)
    print("solve23_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=23, year=2021)


class Mover:
    burrow: dict = None
    initialBurrow: dict = None
    targets: dict = None
    stopPositions: tuple = None
    stopoverPositions: tuple = None
    homePositions: tuple = None
    deepHomePositions: tuple = None
    shallowHomePositions: tuple = None
    podCost: dict = None
    paths: dict = None
    cost = 0
    mincost = maxsize
    best: tuple = ()
    podPositionsToMove: list = None
    debug = 0
    best: None

    def __init__(self, values, debug=0):
        self.debug = debug
        self.initialBurrow = {
            (0, 0): {"moves": [(1, 0)], "pod": None},
            (1, 0): {"moves": [(0, 0), (2, 0)], "pod": None},
            (2, 0): {"moves": [(1, 0), (2, 1), (3, 0)], "pod": None},
            (3, 0): {"moves": [(2, 0), (4, 0)], "pod": None},
            (4, 0): {"moves": [(3, 0), (4, 1), (5, 0)], "pod": None},
            (5, 0): {"moves": [(4, 0), (6, 0)], "pod": None},
            (6, 0): {"moves": [(5, 0), (6, 1), (7, 0)], "pod": None},
            (7, 0): {"moves": [(6, 0), (8, 0)], "pod": None},
            (8, 0): {"moves": [(7, 0), (8, 1), (9, 0)], "pod": None},
            (9, 0): {"moves": [(8, 0), (10, 0)], "pod": None},
            (10, 0): {"moves": [(9, 0)], "pod": None},
            (2, 1): {"moves": [(2, 0), (2, 2)], "pod": None},
            (4, 1): {"moves": [(4, 0), (4, 2)], "pod": None},
            (6, 1): {"moves": [(6, 0), (6, 2)], "pod": None},
            (8, 1): {"moves": [(8, 0), (8, 2)], "pod": None},
            (2, 2): {"moves": [(2, 1)], "pod": None},
            (4, 2): {"moves": [(4, 1)], "pod": None},
            (6, 2): {"moves": [(6, 1)], "pod": None},
            (8, 2): {"moves": [(8, 1)], "pod": None},
        }

        values = values.splitlines()
        self.initialBurrow[(2, 1)]["pod"] = values[2][3]
        self.initialBurrow[(4, 1)]["pod"] = values[2][5]
        self.initialBurrow[(6, 1)]["pod"] = values[2][7]
        self.initialBurrow[(8, 1)]["pod"] = values[2][9]
        self.initialBurrow[(2, 2)]["pod"] = values[3][3]
        self.initialBurrow[(4, 2)]["pod"] = values[3][5]
        self.initialBurrow[(6, 2)]["pod"] = values[3][7]
        self.initialBurrow[(8, 2)]["pod"] = values[3][9]

        self.targets = {
            "A": [(2, 1), (2, 2)],
            "B": [(4, 1), (4, 2)],
            "C": [(6, 1), (6, 2)],
            "D": [(8, 1), (8, 2)],
        }

        self.stopPositions = (
            (0, 0),
            (1, 0),
            (3, 0),
            (5, 0),
            (7, 0),
            (9, 0),
            (10, 0),
            (2, 1),
            (2, 2),
            (4, 1),
            (4, 2),
            (6, 1),
            (6, 2),
            (8, 1),
            (8, 2),
        )
        self.stopoverPositions = (
            (0, 0),
            (1, 0),
            (3, 0),
            (5, 0),
            (7, 0),
            (9, 0),
            (10, 0),
        )
        self.homePositions = (
            (2, 1),
            (2, 2),
            (4, 1),
            (4, 2),
            (6, 1),
            (6, 2),
            (8, 1),
            (8, 2),
        )
        self.deepHomePositions = (
            (2, 2),
            (4, 2),
            (6, 2),
            (8, 2),
        )
        self.shallowHomePositions = (
            (2, 1),
            (4, 1),
            (6, 1),
            (8, 1),
        )
        self.podCost = {
            "A": 1,
            "B": 10,
            "C": 100,
            "D": 1000,
        }
        self.paths = {}

        self.printBurrow(self.initialBurrow)
        self.burrow = self.initialBurrow
        correct = len([pos for pos in self.homePositions
                       if self.initialBurrow[pos]["pod"] and
                       self.initialBurrow[pos] in self.targets[self.initialBurrow[pos]["pod"]]])
        projectedCost = sum([self.podCost[self.initialBurrow[pos]["pod"]] *
            len(self.getPath(pos, self.targets[self.initialBurrow[pos]["pod"]][0], ()))
            for pos in self.stopPositions if self.initialBurrow[pos]["pod"]])
        self.states = [(self.burrowToTuple(self.initialBurrow), self.cost, (), projectedCost, False)]
        for state in self.states:
            self.printState(state, level=1)
        print("paths:")
        pprint(self.paths)
        print("stopPositions:")
        pprint(self.stopPositions)

    def iterateStates(self):
        i = 0
        while self.states:
            i += 1
            self.updateState(self.states.pop(0))
            if (not i % 1000) or self.debug >= 2:
                self.print("states:", len(self.states), "checked:", i, level=1)
                self.print("mincost:", self.mincost, "len(best):", len(self.best), level=1)
                self.printState(self.states[0], level=1)
            if self.debug >= 3:
                print()
                print("all states:")
                for state in self.states:
                    self.printState(state, level=3)
                input()

    def updateState(self, state):
        self.burrow = self.tupleToBurrow(state[0])
        self.cost = state[1]
        moves = state[2]
        projectedCost = state[3]
        # if self.cost >= self.mincost or (self.best and len(moves) > 2 * len(self.best)):
        if self.cost >= self.mincost:
            return
        self.podPositionsToMove = []
        for position in self.deepHomePositions:
            if self.burrow[position]["pod"] is not None:
                above = (position[0], position[1] - 1)
                if position not in self.targets[self.burrow[position]["pod"]]:
                    self.podPositionsToMove.append(position)
                    if self.burrow[above]["pod"] is not None:
                        self.podPositionsToMove.append(above)
                else:
                    if (
                        (self.burrow[above]["pod"] is not None) and
                        (above not in self.targets[self.burrow[above]["pod"]])
                    ):
                        self.podPositionsToMove.append(above)
        for position in self.stopoverPositions:
            if self.burrow[position]["pod"] is not None:
                self.podPositionsToMove.append(position)
        self.print("podPositionsToMove:", self.podPositionsToMove, level=2)
        if not self.podPositionsToMove:
            # no pods left that need to move
            self.print("goal", self.cost, level=0)
            if self.cost < self.mincost:
                self.mincost = self.cost
                self.best = moves
                return

        for position in self.podPositionsToMove:
            targets = self.possibleTargets(position)
            self.print(position, "->", targets, level=2)
            for target in targets:
                self.move(position, target, moves)

    def possibleTargets(self, position):
        targets = []
        for target in self.targets[self.burrow[position]["pod"]]:
            if target == position:
                continue
            if target in self.deepHomePositions:
                targets.append(target)
            elif target in self.shallowHomePositions:
                if (self.burrow[target[0], target[1] + 1]["pod"] ==
                        self.burrow[position]["pod"]):
                    targets.append(target)
        if position in self.stopoverPositions:
            return targets
        return targets + list(self.stopoverPositions)

    def move(self, position, target, moves):
        newBurrow = self.tupleToBurrow(self.burrowToTuple(self.burrow))
        if newBurrow[target]["pod"] is None:
            path = self.getPath(position, target, ())
            self.print(position, "->", target, ":", path, level=2)
            if path is None:
                self.print("no path found to target", level=0)
                input()
            for step in path:
                if newBurrow[step]["pod"] is not None:
                    self.print("someone is in the way", level=2)
                    return
            # valid path
            try:
                cost = self.cost + self.podCost[newBurrow[position]["pod"]] * len(path)
            except Exception:
                self.printBurrow(newBurrow)
                print(position, newBurrow[position]["pod"], len(path))
                raise
            newBurrow[target]["pod"] = newBurrow[position]["pod"]
            newBurrow[position]["pod"] = None
            correct = len([pos for pos in self.homePositions
                           if newBurrow[pos]["pod"] and newBurrow[pos] in self.targets[newBurrow[pos]["pod"]]])
            if correct == 8:
                if cost < self.mincost:
                    self.mincost = cost
                    self.best = moves
                    return
            else:
                projectedCost = sum([self.podCost[newBurrow[pos]["pod"]] *
                    len(self.getPath(pos, self.targets[newBurrow[pos]["pod"]][0], ()))
                    for pos in self.stopPositions if newBurrow[pos]["pod"]])
                insort_left(
                    self.states,
                    (self.burrowToTuple(newBurrow), cost, moves + ((position, target),), projectedCost, target in self.homePositions),
                    key=lambda x: (x[3], x[1])
                )
            return True

    def getPath(self, position: tuple, target: tuple, steps: tuple, from_: tuple = None):
        if (position, target) in self.paths:
            return self.paths[(position, target)]
        for step in self.burrow[position]["moves"]:
            if step == target:
                return steps + (target,)
            elif step == from_:
                continue
            else:
                path = self.getPath(step, target, steps + (step,), position)
                if path:
                    self.paths[(position, target)] = path
                    return path

    def doMoves(self, moves):
        newBurrow = self.tupleToBurrow(self.burrowToTuple(self.initialBurrow))
        for move in moves:
            position, target = move
            newBurrow[target]["pod"] = newBurrow[position]["pod"]
            newBurrow[position]["pod"] = None
            self.printBurrow(newBurrow, 0)

    def burrowToTuple(self, burrow):
        return tuple((k, tuple(val.items())) for k, val in burrow.items())

    def tupleToBurrow(self, t):
        return {k: dict(v) for k, v in t}

    def print(self, *args, how=None, level=1, **kwargs):
        if self.debug >= level:
            if how == "pprint":
                return pprint(*args, **kwargs)
            return print(*args, **kwargs)

    def printBurrow(self, burrow, level=1):
        if self.debug >= level:
            print("#############")
            print(
                "#",
                burrow[(0, 0)]["pod"] if burrow[(0, 0)]["pod"] is not None else ".",
                burrow[(1, 0)]["pod"] if burrow[(1, 0)]["pod"] is not None else ".",
                ".",
                burrow[(3, 0)]["pod"] if burrow[(3, 0)]["pod"] is not None else ".",
                ".",
                burrow[(5, 0)]["pod"] if burrow[(5, 0)]["pod"] is not None else ".",
                ".",
                burrow[(7, 0)]["pod"] if burrow[(7, 0)]["pod"] is not None else ".",
                ".",
                burrow[(9, 0)]["pod"] if burrow[(9, 0)]["pod"] is not None else ".",
                burrow[(10, 0)]["pod"] if burrow[(10, 0)]["pod"] is not None else ".",
                "#", sep=""
            )
            print(
                "###",
                burrow[(2, 1)]["pod"] if burrow[(2, 1)]["pod"] is not None else ".",
                "#",
                burrow[(4, 1)]["pod"] if burrow[(4, 1)]["pod"] is not None else ".",
                "#",
                burrow[(6, 1)]["pod"] if burrow[(6, 1)]["pod"] is not None else ".",
                "#",
                burrow[(8, 1)]["pod"] if burrow[(8, 1)]["pod"] is not None else ".",
                "###", sep=""
            )
            print(
                "  #",
                burrow[(2, 2)]["pod"] if burrow[(2, 2)]["pod"] is not None else ".",
                "#",
                burrow[(4, 2)]["pod"] if burrow[(4, 2)]["pod"] is not None else ".",
                "#",
                burrow[(6, 2)]["pod"] if burrow[(6, 2)]["pod"] is not None else ".",
                "#",
                burrow[(8, 2)]["pod"] if burrow[(8, 2)]["pod"] is not None else ".",
                "#", sep=""
            )
            print("  #########")

    def printState(self, state, level=2):
        if self.debug >= level:
            try:
                print("state:")
                self.printBurrow(self.tupleToBurrow(state[0]))
                print("cost:", state[1])
                print(f"moves({len(state[2])}):", state[2])
                print()
            except Exception as e:
                print("exception", e)
                print(state)
                raise


def solve23(values):
    mover = Mover(values, debug=1)
    mover.iterateStates()
    print("\n========================\n")
    print("best:", mover.best)
    mover.doMoves(mover.best)
    return mover.mincost


def solve23_2(values):
    ...


if __name__ == "__main__":
    main()
