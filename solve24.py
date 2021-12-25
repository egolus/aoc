#!/bin/env python
import itertools
from aocd import get_data, submit


def main():
    values = get_data(day=24, year=2021)
    testvalues = ""
    testtrue = 0
    testtrue2 = 0

    # testresult = solve24(testvalues)
    # assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve24(values)
    print("solve24:", result)

    # input("submit?")
    submit(result, part="a", day=24, year=2021)

    testresult2 = solve24_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve24_2(values)
    print("solve24_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=24, year=2021)


def ALU(no, monad, j=0):
    model = str(no)
    if "0" in model:
        raise ValueError()
    if not j % 1000:
        print(model, end="\r")
    pos = 0
    registers = {"w": 0, "x": 0, "y": 0, "z": 0}
    for line in monad:
        if line[0] == "inp":
            registers[line[1]] = int(model[pos])
            pos += 1
        elif line[0] == "add":
            try:
                registers[line[1]] += int(line[2])
            except ValueError:
                registers[line[1]] += registers[line[2]]
        elif line[0] == "mul":
            try:
                registers[line[1]] *= int(line[2])
            except ValueError:
                registers[line[1]] *= registers[line[2]]
        elif line[0] == "div":
            try:
                registers[line[1]] //= int(line[2])
            except ValueError:
                registers[line[1]] //= registers[line[2]]
        elif line[0] == "mod":
            try:
                registers[line[1]] %= int(line[2])
            except ValueError:
                registers[line[1]] %= registers[line[2]]
        elif line[0] == "eql":
            try:
                registers[line[1]] = (
                    1 if registers[line[1]] == int(line[2]) else 0
                )
            except ValueError:
                registers[line[1]] = (
                    1 if registers[line[1]] == registers[line[2]] else 0
                )
    return registers


def solve24(values, debug=False):
    monad = [line.split(" ") for line in values.splitlines()]
    print(monad)
    highest = 0
    j = 0
    ignoredDigits = []
    base = None
    for i, no in enumerate(
        (
            "11111111111111",
            "21111111111111",
            "12111111111111",
            "11211111111111",
            "11121111111111",
            "11112111111111",
            "11111211111111",
            "11111121111111",
            "11111112111111",
            "11111111211111",
            "11111111121111",
            "11111111112111",
            "11111111111211",
            "11111111111121",
            "11111111111112",
        )
    ):
        j += 1
        registers = ALU(no, monad, j)
        if registers["z"] == 0:
            print(no, "valid")
            return highest
        if not base:
            base = {
                "w": registers["w"],
                "x": registers["x"],
                "y": registers["y"],
                "z": registers["z"],
            }
        else:
            if all(registers[c] == base[c] for c in ["w","x", "y", "z"]):
                print(f"digit {i} doesn't matter")
                ignoredDigits.append(i)
    digits = []
    perms = [[]]
    for i in range(14):
        if i in ignoredDigits:
            perms = [perm + [9] for perm in perms]
        else:
            newperms = []
            for j in range(9, 0, -1):
                newperms += tuple([perm + [j] for perm in perms])
            perms = newperms
        print(i, len(perms))
    j = -1
    print(perms[:10])
    for no in perms:
        for i in range(9, 0, -1):
            j += 1
            try:
                registers = ALU("".join(str(x) for x in no)+str(i), monad, j)
            except ValueError:
                print("valueError")
                # continue
                return
            if registers["z"] == 0:
                return "".join(no)


def solve24_2(values):
    ...


if __name__ == "__main__":
    main()
