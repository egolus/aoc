#!/bin/env python
from aocd import get_data, submit


def main():
    values = get_data(day=10, year=2021).split("\n")
    testvalues = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".split("\n")
    testtrue = 26397
    testtrue2 = 288957

    testresult = solve10(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve10(values)
    print("solve10:", result)

    # input("submit?")
    submit(result, part="a", day=10, year=2021)

    testresult2 = solve10_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve10_2(values)
    print("solve10_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=10, year=2021)


def solve10(lines):
    result = 0
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<",
    }
    score = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    chunks = []
    for i, line in enumerate(lines):
        stop = False
        for c in line:
            if c in "([{<":
                # opening chunk
                chunks.append(c)
            elif c in ")]}>":
                if chunks[-1] == pairs[c]:
                    # closing chunk
                    chunks.pop(-1)
                else:
                    result += score[c]
                    print(i, line, c, score[c], result)
                    stop = True
                    break
        if stop:
            continue
    return result


def legal(line):
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<",
    }
    score = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    chunks = []
    for c in line:
        if c in "([{<":
            # opening chunk
            chunks.append(c)
        elif c in ")]}>":
            if chunks[-1] == pairs[c]:
                # closing chunk
                chunks.pop(-1)
            else:
                return False
    else:
        return True


def solve10_2(lines):
    results = []
    legalLines = [line for line in lines if legal(line)]
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<",
    }
    score = {
        "(": 1,
        "[": 2,
        "{": 3,
        "<": 4,
    }
    for i, line in enumerate(legalLines):
        chunks = []
        res = 0
        for c in line:
            if c in "([{<":
                # opening chunk
                chunks.append(c)
            elif c in ")]}>":
                if chunks[-1] == pairs[c]:
                    # closing chunk
                    chunks.pop(-1)
                else:
                    chunks.append(c)
        print(chunks)
        for chunk in reversed(chunks):
            res = (5 * res) + score[chunk]
            print(res, chunk)
        results.append(res)
    return sorted(results)[len(results)//2]


if __name__ == "__main__":
    main()
