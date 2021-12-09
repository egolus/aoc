#!/bin/env python
from aocd import get_data, submit


def main():
    values = get_data(day=8, year=2021).split("\n")
    testvalues = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".split("\n")
    testtrue = 26
    testvalues2 = """fdgacbe cefdb cefbgd gcbe
fcgedb cgb dgebacf gc
cg cg fdcagb cbg
efabcd cedba gadfec cb
gecf egdcabf bgf bfgea
gebdcfa ecba ca fadegcb
cefg dcbef fcge gbcadfe
ed bcgafe cdgba cbgef
gbdfcae bgc cg cgb
fgae cfgab fg bagce""".split("\n")
    testtrue2 = 61229 + 5353

    testresult = solve08(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve08(values)
    print("solve08:", result)

    # input("submit?")
    submit(result, part="a", day=8, year=2021)

    testresult2 = solve08_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve08_2(values)
    print("solve08_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=8, year=2021)


def solve08(lines):
    result = 0
    digitlengths = {
        2: 1,
        7: 8,
        4: 4,
        3: 7,
    }
    for line in lines:
        output = line.split("|")[1]
        outputdigits = output.split(" ")
        for digit in outputdigits:
            if len(digit) in digitlengths:
                result += 1
    return result


class Solver():
    """
      -> 1
      -> 4
      -> 7
      -> 8
    a = 7 - 1
    g = ((2|3|5) - 1 == 3) - 4
      -> 3
    d = 3 - 1 != g
    e = (2|5) - 4 != a
      -> 5
      -> 6 = 5 + e
    c = 8 - 6
      -> 9 = 5 + c
      -> 0 = 7 + b + e
    """
    result = 0
    digits = None
    solvedDigits = None
    segments = None

    def __init__(self, line):
        self.digits = set()
        self.solvedDigits = {}
        self.segments = {}
        for digit in line.split(" "):
            digit = "".join(sorted(s for s in digit))
            self.digits.add(digit)
        print(self.digits)

    def getDigit(self, d):
        if d in self.solvedDigits:
            return self.solvedDigits[d]

    def sub(self, x, y):
        if type(x) is not str:
            cx = self.getDigit(x)
        else:
            cx = x
        cy = self.getDigit(y)
        rest = [c for c in cx if c not in cy]
        # print(x, y, cx, cy, "->", rest)
        return "".join(rest)

    def add(self, d, s):
        # print(f"add - d: {d}, s: {s}")
        if type(d) is not list:
            return sorted([x for x in self.solvedDigits[d]] + [self.segments[s]])
        return sorted([x for x in d] + [self.segments[s]])

    def solve(self):
        self.solvedDigits[1] = next(d for d in self.digits if len(d) == 2)
        self.solvedDigits[4] = next(d for d in self.digits if len(d) == 4)
        self.solvedDigits[7] = next(d for d in self.digits if len(d) == 3)
        self.solvedDigits[8] = next(d for d in self.digits if len(d) == 7)

        # seg a
        self.segments["a"] = self.sub(7, 1)
        # seg g
        d235 = [d for d in self.digits if len(d) == 5]
        self.solvedDigits[3] = next(d for d in d235
                                    if len(self.sub(d, 1)) == 3)
        self.segments["g"] = self.sub(self.sub(3, 7), 4)
        segs = self.sub(3, 1)
        self.segments["d"] = next(seg for seg in segs
                                  if seg != self.segments["g"]
                                  and seg != self.segments["a"])
        for d in d235:
            if d != self.solvedDigits[3]:
                if len(self.sub(d, 4)) == 2:
                    self.solvedDigits[5] = d
                    self.segments["b"] = self.sub(d, 3)
                else:
                    self.solvedDigits[2] = d
                    self.segments["e"] = self.sub(self.sub(d, 4), 3)
        self.solvedDigits[6] = "".join(self.add(5, "e"))
        self.segments["c"] = self.sub(8, 6)
        self.solvedDigits[9] = "".join(self.add(5, "c"))

        self.solvedDigits[0] = "".join(self.add(self.add(self.add(7, "b"), "e"), "g"))

        print("solved digits:", self.solvedDigits)
        print("segments:", self.segments)

    def result(self, line):
        res = ""
        for digit in line.split(" "):
            digit = "".join(sorted(s for s in digit))
            for k, v in self.solvedDigits.items():
                if v == digit:
                    print(digit, k)
                    res += str(k)
        print(res)
        return int(res)


def solve08_2(lines):
    result = 0
    for line in lines:
        split = line.split(" | ")
        solver = Solver(split[0])
        solver.solve()
        result += solver.result(split[1])
    return result


def solve08_2_old(lines):
    result = 0
    digitlengths = {
        # 2: "cf",
        # 3: "acf",
        # 4: "bcdf",
        7: "abcdefg",
    }
    segments = {
        "abcefg": 0,
        "cf": 1,
        "acdeg": 2,
        "acdfg": 3,
        "bcdf": 4,
        "abdfg": 5,
        "abdefg": 6,
        "acf": 7,
        "abcdefg": 8,
        "abcdfg": 9,
    }
    parsedlines = []
    chars = {}
    for line in lines:
        if "|" in line:
            output = line.split("|")[1]
        else:
            output = line
        outputdigits = output.split(" ")
        parsedlines.append(outputdigits)
    for line in parsedlines:
        for digit in line:
            # if len(digit) in digitlengths:
                # for i, c in enumerate(digit):
                    # chars[c] = digitlengths[len(digit)][i]
                # if len(chars) == 9:
                    # break
            if len(digit) == 7:
                for i, char in enumerate(digit):
                    chars[char] = "abcdefg"[i]
    print("chars", chars)
    for line in parsedlines:
        for digit in line:
            outchars = ""
            for char in digit:
                outchars += chars[char]
            result += segments["".join(sorted(outchars))]
    return result


if __name__ == "__main__":
    main()
