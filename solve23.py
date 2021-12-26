#!/bin/env python
from sys import maxsize
from bisect import insort_left
from aocd import get_data, submit
from pprint import pprint
import json


def main():
    values = get_data(day=23, year=2021)
    testvalues = {
        ("#############\n"
         "#...........#\n"
         "###B#A#C#D###\n"
         "  #A#B#C#D#\n"
         "  #########", 1): 46,
        ("#############\n"
         "#...........#\n"
         "###B#A#C#D###\n"
         "  #B#A#C#D#\n"
         "  #########", 1): 114,
        ("#############\n"
         "#...........#\n"
         "###B#C#B#D###\n"
         "  #A#D#C#A#\n"
         "  #########", 1): 12521,
    }
    testvalues2 = {
        ("#############\n"
        "#...........#\n"
        "###B#C#B#D###\n"
        "  #D#C#B#A#\n"
        "  #A#D#C#A#\n"
        "  #A#D#C#A#"
        "  #########", 1): 44169,
    }

    #for test, true in testvalues.items():
    #    testresult = solve23(*test)
    #    assert testresult == true, f"{testresult} != {true}"
    #result = solve23(values)
    #print("solve23:", result)

    # input("submit?")
    #submit(result, part="a", day=23, year=2021)

    for test, true in testvalues2.items():
        testresult = solve23_2(*test)
        assert testresult == true, f"{testresult} != {true}"
    result2 = solve23_2(values)
    print("solve23_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=23, year=2021)


burrow_sm = {
    (0, 0): {"moves": [(1, 0)]},
    (1, 0): {"moves": [(0, 0), (2, 0)]},
    (2, 0): {"moves": [(1, 0), (2, 1), (3, 0)]},
    (3, 0): {"moves": [(2, 0), (4, 0)]},
    (4, 0): {"moves": [(3, 0), (4, 1), (5, 0)]},
    (5, 0): {"moves": [(4, 0), (6, 0)]},
    (6, 0): {"moves": [(5, 0), (6, 1), (7, 0)]},
    (7, 0): {"moves": [(6, 0), (8, 0)]},
    (8, 0): {"moves": [(7, 0), (8, 1), (9, 0)]},
    (9, 0): {"moves": [(8, 0), (10, 0)]},
    (10, 0): {"moves": [(9, 0)]},
    (2, 1): {"moves": [(2, 0), (2, 2)]},
    (4, 1): {"moves": [(4, 0), (4, 2)]},
    (6, 1): {"moves": [(6, 0), (6, 2)]},
    (8, 1): {"moves": [(8, 0), (8, 2)]},
    (2, 2): {"moves": [(2, 1)]},
    (4, 2): {"moves": [(4, 1)]},
    (6, 2): {"moves": [(6, 1)]},
    (8, 2): {"moves": [(8, 1)]},
}
burrow_ex = {
    (0, 0): {"moves": [(1, 0)]},
    (1, 0): {"moves": [(0, 0), (2, 0)]},
    (2, 0): {"moves": [(1, 0), (2, 1), (3, 0)]},
    (3, 0): {"moves": [(2, 0), (4, 0)]},
    (4, 0): {"moves": [(3, 0), (4, 1), (5, 0)]},
    (5, 0): {"moves": [(4, 0), (6, 0)]},
    (6, 0): {"moves": [(5, 0), (6, 1), (7, 0)]},
    (7, 0): {"moves": [(6, 0), (8, 0)]},
    (8, 0): {"moves": [(7, 0), (8, 1), (9, 0)]},
    (9, 0): {"moves": [(8, 0), (10, 0)]},
    (10, 0): {"moves": [(9, 0)]},
    (2, 1): {"moves": [(2, 0), (2, 2)]},
    (4, 1): {"moves": [(4, 0), (4, 2)]},
    (6, 1): {"moves": [(6, 0), (6, 2)]},
    (8, 1): {"moves": [(8, 0), (8, 2)]},
    (2, 2): {"moves": [(2, 1), (2, 3)]},
    (4, 2): {"moves": [(4, 1), (4, 3)]},
    (6, 2): {"moves": [(6, 1), (6, 3)]},
    (8, 2): {"moves": [(8, 1), (8, 3)]},
    (2, 3): {"moves": [(2, 2), (2, 4)]},
    (4, 3): {"moves": [(4, 2), (4, 4)]},
    (6, 3): {"moves": [(6, 2), (6, 4)]},
    (8, 3): {"moves": [(8, 2), (8, 4)]},
    (2, 4): {"moves": [(2, 3)]},
    (4, 4): {"moves": [(4, 3)]},
    (6, 4): {"moves": [(6, 3)]},
    (8, 4): {"moves": [(8, 3)]},
}

targets_sm = {
    "A": [(2, 1), (2, 2)],
    "B": [(4, 1), (4, 2)],
    "C": [(6, 1), (6, 2)],
    "D": [(8, 1), (8, 2)],
}

targets_ex = {
    "A": [(2, 1), (2, 2), (2, 3), (2, 4)],
    "B": [(4, 1), (4, 2), (4, 3), (4, 4)],
    "C": [(6, 1), (6, 2), (6, 3), (6, 4)],
    "D": [(8, 1), (8, 2), (8, 3), (8, 4)],
}

stopPositions_sm = (
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
stopPositions_ex = (
    (0, 0),
    (1, 0),
    (3, 0),
    (5, 0),
    (7, 0),
    (9, 0),
    (10, 0),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (4, 1),
    (4, 2),
    (4, 3),
    (4, 4),
    (6, 1),
    (6, 2),
    (6, 3),
    (6, 4),
    (8, 1),
    (8, 2),
    (8, 3),
    (8, 4),
)
stopoverPositions_sm = (
    (0, 0),
    (1, 0),
    (3, 0),
    (5, 0),
    (7, 0),
    (9, 0),
    (10, 0),
)
homePositions_sm = (
    (2, 1),
    (2, 2),
    (4, 1),
    (4, 2),
    (6, 1),
    (6, 2),
    (8, 1),
    (8, 2),
)
homePositions_ex = (
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (4, 1),
    (4, 2),
    (4, 3),
    (4, 4),
    (6, 1),
    (6, 2),
    (6, 3),
    (6, 4),
    (8, 1),
    (8, 2),
    (8, 3),
    (8, 4),
)
podCost = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


class Mover:
    openSet: dict = None
    cameFrom: dict = None
    # cost of the cheapest path from start to here (currently known)
    gScore: dict = None
    # best guess of cost for a path going through here to the exit
    fScore: dict = None
    start: tuple = None
    goal: tuple = None
    state: tuple = None
    stateDict: dict = None
    d: dict = None
    debug = False
    ex = False
    cost: int = None
    burrow: dict = None
    targets: dict = None
    stopPositions: tuple = None
    stopoverPositions: tuple = None
    homePositions: tuple = None
    podCost: dict = None
    podPath: dict = None

    def __init__(self, start, goal, ex=False, debug=False):
        start = tuple(sorted(start))
        goal = tuple(sorted(goal))
        self.start = start
        self.goal = goal
        self.openSet = {start}
        self.cameFrom = {}
        self.gScore = {start: 0}
        self.fScore = {start: 0}
        self.ex = ex
        self.targets = targets_sm if not ex else targets_ex
        self.stopPositions = stopPositions_sm if not ex else stopPositions_ex
        self.stopoverPositions = stopoverPositions_sm
        self.homePositions = homePositions_sm if not ex else homePositions_ex
        self.burrow = burrow_sm if not ex else burrow_ex
        self.podCost = podCost
        self.podPath = {}
        self.d = {}
        if debug is None:
            self.debug = 0
        else:
            self.debug = debug
        self.getPaths()

    def solve(self):
        count = 0
        while self.openSet:
            count += 1
            self.print("==============\n", level=3)
            self.print("self.openSet:", level=2)
            self.print(len(self.openSet), level=2)
            if self.debug >= 3:
                for k in sorted(self.openSet,
                                key=lambda a: self.fScore.get(a, maxsize)):
                    v = self.gScore[k]
                    self.print(level=3)
                    self.printBurrow(k, level=3)
                    self.print("cost:", v, level=3)
                    self.print("fScore:", self.fScore[k], level=3)
                input()
            self.state = min(self.openSet,
                             key=lambda a: self.fScore.get(a, maxsize))
            self.stateDict = dict(self.state)
            if not count % 500 and self.debug:
                self.printBurrow()
                print("len(self.openSet):", len(self.openSet))
                print("gScore:", self.gScore[self.state])
            if self.state == self.goal:
                print("found a path")
                self.cost = self.gScore[self.goal]
                return self.reconstructPath()
            self.openSet.remove(self.state)
            for neighbor in self.getNeighbors():
                tentativeGScore = self.gScore[self.state] + \
                        self.d[self.state, neighbor]
                if ((neighbor not in self.gScore) or
                        (tentativeGScore < self.gScore[neighbor])):
                    self.cameFrom[neighbor] = self.state
                    self.gScore[neighbor] = tentativeGScore
                    self.fScore[neighbor] = tentativeGScore + self.h(neighbor)
                    self.openSet.add(neighbor)
        print("no path found")

    def getNeighbors(self):
        # get all valid moves for the pods in the current state and return the
        # resulting states
        neighbors = []
        positionsToMove = []
        for pos, pod in self.state:
            if pos in self.homePositions:
                if pos not in self.targets[pod]:
                    positionsToMove.append((pos, pod))
                below = [(p, pd) for p, pd in self.state
                         if p[0] == pos[0] and p[1] > pos[1] and pd != pod]
                if below:
                    positionsToMove.append((pos, pod))
            else:
                positionsToMove.append((pos, pod))
        for position, pod in positionsToMove:
            for target in self.possibleTargets(position, pod):
                self.print("found target:", target, level=3)
                if self.debug >= 3:
                    print([(s, self.stateDict.get(s, None)) for s
                           in self.podPath.get((position, target), None)])
                if any([self.stateDict.get(s, None) for s
                        in self.podPath.get((position, target), None)]):
                    self.print("blocked:", level=3)
                    continue
                else:
                    cost = self.podCost[pod] * len(self.podPath[(position, target)])
                    newState = {k: v for k, v in self.state}
                    newState.pop(position)
                    newState[target] = pod
                    newState = tuple(sorted(newState.items()))
                    self.d[(self.state, newState)] = cost
                    neighbors.append(newState)
        return neighbors

    def possibleTargets(self, position, pod):
        podTargets = []
        self.print("position:", position, level=3)
        for target in self.targets[pod]:
            self.print("target:", target, level=3)
            if target[0] == position[0]:
                self.print("!target == position", level=3)
                continue
            below = [p for p in self.targets[pod] if
                     p[1] > target[1] and self.stateDict.get(p, None) != pod]
            self.print("pod:", pod, level=3)
            self.print("below", below, [self.stateDict.get(p, None)
                                        for p in below], level=3)
            if not below:
                self.print("valid", level=3)
                podTargets.append(target)
        if position in self.stopoverPositions:
            self.print("stopover -> home", level=3)
            return podTargets
        self.print("home -> home/stopover", level=3)
        return podTargets + list(self.stopoverPositions)

    def getPaths(self):
        for position in self.stopPositions:
            for target in self.stopPositions:
                self.podPath[position, target] = self.getPath(position, target, ())

    def getPath(self, position: tuple, target: tuple, steps: tuple, from_: tuple = None):
        for step in self.burrow[position]["moves"]:
            if step == target:
                return steps + (target, )
            elif step == from_:
                continue
            else:
                path = self.getPath(step, target, steps + (step,), position)
                if path:
                    return path

    def h(self, node):
        # estimate the cost to reach the goal from this node
        return 500 * sum([self.podCost[val] * len(self.podPath[key, self.targets[val][0]])
                    for key, val in node if key not in self.targets[val]])

    def reconstructPath(self, node=None):
        # get the path from the start to this node
        if node is None:
            node = self.state
        path = [node]
        while node in self.cameFrom.keys():
            node = self.cameFrom[node]
            path = [node] + path
        return path

    def print(self, *args, level=None, **kwargs):
        if level is None:
            level = 1
        if level <= self.debug:
            print(*args, **kwargs)

    def printBurrow(self, state=None, level=None):
        if state is not None:
            stateDict = dict(state)
        else:
            stateDict = self.stateDict
        self.print("#############", level=level, end="   ")
        if state in self.cameFrom:
            self.print("#############", level=level)
        else:
            self.print(level=level)
        self.print(
            "#",
            stateDict[(0, 0)] if (0, 0) in stateDict else ".",
            stateDict[(1, 0)] if (1, 0) in stateDict else ".",
            ".",
            stateDict[(3, 0)] if (3, 0) in stateDict else ".",
            ".",
            stateDict[(5, 0)] if (5, 0) in stateDict else ".",
            ".",
            stateDict[(7, 0)] if (7, 0) in stateDict else ".",
            ".",
            stateDict[(9, 0)] if (9, 0) in stateDict else ".",
            stateDict[(10, 0)] if (10, 0) in stateDict else ".",
            "#", sep="", end="   ",
            level=level
        )
        if state in self.cameFrom:
            self.print(
                "#",
                dict(self.cameFrom[state]).get((0, 0), "."),
                dict(self.cameFrom[state]).get((1, 0), "."),
                ".",
                dict(self.cameFrom[state]).get((3, 0), "."),
                ".",
                dict(self.cameFrom[state]).get((5, 0), "."),
                ".",
                dict(self.cameFrom[state]).get((7, 0), "."),
                ".",
                dict(self.cameFrom[state]).get((9, 0), "."),
                dict(self.cameFrom[state]).get((10, 0), "."),
                "#", sep="",
                level=level
            )
        else:
            self.print(level=level)
        self.print(
            "###",
            stateDict[(2, 1)] if (2, 1) in stateDict else ".",
            "#",
            stateDict[(4, 1)] if (4, 1) in stateDict else ".",
            "#",
            stateDict[(6, 1)] if (6, 1) in stateDict else ".",
            "#",
            stateDict[(8, 1)] if (8, 1) in stateDict else ".",
            "###", sep="", end="   ",
            level=level
        )
        if state in self.cameFrom:
            self.print(
                "###",
                dict(self.cameFrom[state]).get((2, 1), "."),
                "#",
                dict(self.cameFrom[state]).get((4, 1), "."),
                "#",
                dict(self.cameFrom[state]).get((6, 1), "."),
                "#",
                dict(self.cameFrom[state]).get((8, 1), "."),
                "###", sep="",
                level=level
            )
        else:
            self.print(level=level)
        self.print(
            "  #",
            stateDict[(2, 2)] if (2, 2) in stateDict else ".",
            "#",
            stateDict[(4, 2)] if (4, 2) in stateDict else ".",
            "#",
            stateDict[(6, 2)] if (6, 2) in stateDict else ".",
            "#",
            stateDict[(8, 2)] if (8, 2) in stateDict else ".",
            "#", sep="", end="     ",
            level=level
        )
        if state in self.cameFrom:
            self.print(
                "  #",
                dict(self.cameFrom[state]).get((2, 2), "."),
                "#",
                dict(self.cameFrom[state]).get((4, 2), "."),
                "#",
                dict(self.cameFrom[state]).get((6, 2), "."),
                "#",
                dict(self.cameFrom[state]).get((8, 2), "."),
                "#", sep="",
                level=level
            )
        else:
            self.print(level=level)
        self.print(
            "  #",
            stateDict[(2, 3)] if (2, 3) in stateDict else ".",
            "#",
            stateDict[(4, 3)] if (4, 3) in stateDict else ".",
            "#",
            stateDict[(6, 3)] if (6, 3) in stateDict else ".",
            "#",
            stateDict[(8, 3)] if (8, 3) in stateDict else ".",
            "#", sep="", end="     ",
            level=level
        )
        if state in self.cameFrom:
            self.print(
                "  #",
                dict(self.cameFrom[state]).get((2, 3), "."),
                "#",
                dict(self.cameFrom[state]).get((4, 3), "."),
                "#",
                dict(self.cameFrom[state]).get((6, 3), "."),
                "#",
                dict(self.cameFrom[state]).get((8, 3), "."),
                "#", sep="",
                level=level
            )
        else:
            self.print(level=level)
        self.print(
            "  #",
            stateDict[(2, 4)] if (2, 4) in stateDict else ".",
            "#",
            stateDict[(4, 4)] if (4, 4) in stateDict else ".",
            "#",
            stateDict[(6, 4)] if (6, 4) in stateDict else ".",
            "#",
            stateDict[(8, 4)] if (8, 4) in stateDict else ".",
            "#", sep="", end="     ",
            level=level
        )
        if state in self.cameFrom:
            self.print(
                "  #",
                dict(self.cameFrom[state]).get((2, 4), "."),
                "#",
                dict(self.cameFrom[state]).get((4, 4), "."),
                "#",
                dict(self.cameFrom[state]).get((6, 4), "."),
                "#",
                dict(self.cameFrom[state]).get((8, 4), "."),
                "#", sep="",
                level=level
            )
        else:
            self.print(level=level)
        self.print("  #########  ", level=level, end="   ")
        if state in self.cameFrom:
            self.print("  #########  ", level=level)
        else:
            self.print(level=level)


def solve23(values, debug=None):
    values = values.splitlines()
    start = (
        ((2, 1), values[2][3]),
        ((4, 1), values[2][5]),
        ((6, 1), values[2][7]),
        ((8, 1), values[2][9]),
        ((2, 2), values[3][3]),
        ((4, 2), values[3][5]),
        ((6, 2), values[3][7]),
        ((8, 2), values[3][9]),
    )
    goal = (
        ((2, 1), "A"),
        ((4, 1), "B"),
        ((6, 1), "C"),
        ((8, 1), "D"),
        ((2, 2), "A"),
        ((4, 2), "B"),
        ((6, 2), "C"),
        ((8, 2), "D"),
    )
    mover = Mover(start, goal, debug=debug)
    path = mover.solve()
    for s in path:
        mover.printBurrow(s)
    print("score:", mover.gScore[tuple(sorted(goal))])
    print("score:", mover.cost)
    return mover.cost


def solve23_2(values, debug=None):
    values = values.splitlines()
    #  #D#C#B#A#
    #  #D#B#A#C#
    start = (
        ((2, 1), values[2][3]),
        ((4, 1), values[2][5]),
        ((6, 1), values[2][7]),
        ((8, 1), values[2][9]),
        ((2, 2), "D"),
        ((4, 2), "C"),
        ((6, 2), "B"),
        ((8, 2), "A"),
        ((2, 3), "D"),
        ((4, 3), "C"),
        ((6, 3), "A"),
        ((2, 4), values[3][3]),
        ((4, 4), values[3][5]),
        ((6, 4), values[3][7]),
        ((8, 4), values[3][9]),
    )
    goal = (
        ((2, 1), "A"),
        ((4, 1), "B"),
        ((6, 1), "C"),
        ((8, 1), "D"),
        ((2, 2), "A"),
        ((4, 2), "B"),
        ((6, 2), "C"),
        ((8, 2), "D"),
    )
    mover = Mover(start, goal, ex=True, debug=debug)
    path = mover.solve()
    for s in path:
        mover.printBurrow(s)
    print("score:", mover.gScore[tuple(sorted(goal))])
    print("score:", mover.cost)
    return mover.cost



if __name__ == "__main__":
    main()
