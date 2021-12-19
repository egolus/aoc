#!/bin/env python
from itertools import permutations
from json import loads
from aocd import get_data, submit


def main():
    values = get_data(day=18, year=2021)
    testvalues = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
    testtrue = 4140
    testtrue2 = 3993

    testParse = {
        "[1,2]": [1,2],
        "[[1,2],3]": [[1,2],3],
        "[9,[8,7]]": [9,[8,7]],
        "[[1,9],[8,5]]": [[1,9],[8,5]],
        "[[[[1,2],[3,4]],[[5,6],[7,8]]],9]": [[[[1,2],[3,4]],[[5,6],[7,8]]],9],
        "[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]": [[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]],
        "[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]": [[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]],
    }

    testMagnitude = {
        "[[1,2],[[3,4],5]]": 143,
        "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]": 1384,
        "[[[[1,1],[2,2]],[3,3]],[4,4]]": 445,
        "[[[[3,0],[5,3]],[4,4]],[5,5]]": 791,
        "[[[[5,0],[7,4]],[5,5]],[6,6]]": 1137,
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]": 3488,
    }

    testAdd = {
        ("[1,1]", "[2,2]"): [[1,1],[2,2]],

        ("[1,1]", "[2,2]", "[3,3]", "[4,4]"): [[[[1,1],[2,2]],[3,3]],[4,4]],
        ("[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"): [[[[3,0],[5,3]],[4,4]],[5,5]],
        ("[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6,6]"): [[[[5,0],[7,4]],[5,5]],[6,6]],

        ("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]"): [[[[0,7],4],[[7,8],[6,0]]],[8,1]],
        ("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]", "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]"): [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],
        ("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]", "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]"): [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],
        ("[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]", "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]"): [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],
        ("[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]", "[7,[5,[[3,8],[1,4]]]]"): [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]],
        ("[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]", "[[2,[2,2]],[8,[8,1]]]"): [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]],
        ("[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]", "[2,9]"): [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]],
        ("[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]", "[1,[[[9,3],9],[[9,0],[0,7]]]]"): [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]],
        ("[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]", "[[[5,[7,4]],7],1]"): [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]],
        ("[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]", "[[[[4,2],2],6],[8,7]]"): [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]],
    }

    testExplode = {
        "[[[[[9,8],1],2],3],4]": [[[[0,9],2],3],4],
        "[7,[6,[5,[4,[3,2]]]]]": [7,[6,[5,[7,0]]]],
        "[[6,[5,[4,[3,2]]]],1]": [[6,[5,[7,0]]],3],
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]": [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]],
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]" : [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]],
        "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]": [[3,[2,[8,0]]],[9,[5,[7,0]]]],
    }

    # for test, true in testParse.items():
        # res = parse(test)
        # assert res == true, f"{res} != {true}"

    # for test, true in testMagnitude.items():
        # res = magnitude(parse(test))
        # assert res == true, f"{res} != {true}"

    # for test, true in testExplode.items():
        # it = parse(test)
        # it.checkExplode()
        # assert it == true, f"{it} != {true}"

    for test, true in testAdd.items():
        try:
            res = parse(test[0])
            for it in test[1:]:
                res = add(res, parse(it))
        except:
            print(test[0], test[1])
            raise
        assert res == true, f"{res} != {true}"

    testresult = solve18(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve18(values)
    print("solve18:", result)

    # input("submit?")
    submit(result, part="a", day=18, year=2021)

    testresult2 = solve18_2(testvalues)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve18_2(values)
    print("solve18_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=18, year=2021)


class Pair():
    left = None
    right = None
    parent = None

    def __init__(self, number: list, parent=None):
        left, right = number
        if parent:
            self.parent = parent
        if type(left) is int:
            self.left = left
        else:
            self.left = Pair(left, self)
        if type(right) is int:
            self.right = right
        else:
            self.right = Pair(right, self)

    def checkExplode(self):
        if type(self.left) is int and type(self.right) is int and (
                self.parent and self.parent.parent and self.parent.parent.parent
                and self.parent.parent.parent.parent):
            self.explode()
            return True
        if type(self.left) is Pair:
            reduced = self.left.checkExplode()
            if reduced:
                return True
        if type(self.right) is Pair:
            reduced = self.right.checkExplode()
            if reduced:
                return True

    def explode(self):
        print("exploding", self)
        if self.parent:
            left, right = self.left, self.right
            self.addleft(left)
            self.addright(right)
        if self.parent.left == self:
            self.parent.left = 0
        else:
            self.parent.right = 0
        return True

    def split(self):
        if type(self.left) is int:
            if self.left >= 10:
                print("splitting", self.left)
                n = self.left
                self.left = Pair([n // 2, (n + 1) // 2], self)
                return True
        else:
            if self.left.split():
                return True
        if type(self.right) is int:
            if self.right >= 10:
                print("splitting", self.right)
                n = self.right
                self.right = Pair([n // 2, (n + 1) // 2], self)
                return True
        else:
            if self.right.split():
                return True

    def addleft(self, value):
        if not self.parent:
            return
        if self.parent.right == self and self.parent.left != self.parent.right:
            if type(self.parent.left) == int:
                self.parent.left += value
            else:
                self.parent.left.addinright(value)
        else:
            self.parent.addleft(value)

    def addright(self, value):
        if not self.parent:
            return
        if self.parent.left == self:
            if type(self.parent.right) == int:
                self.parent.right += value
            else:
                self.parent.right.addinleft(value)
        else:
            self.parent.addright(value)

    def addinleft(self, value):
        if type(self.left) is int:
            self.left += value
        else:
            self.left.addinleft(value)

    def addinright(self, value):
        if type(self.right) is int:
            self.right += value
        else:
            self.right.addinright(value)

    def __getattr__(self, name):
        if name == 0:
            return self.left
        if name == 1:
            return self.right

    def __repr__(self):
        return f"[{self.left}, {self.right}]"

    def aslist(self):
        left = self.left.aslist() if type(self.left) is Pair else self.left
        right = self.right.aslist() if type(self.right) is Pair else self.right
        return [left, right]

    def __eq__(self, other):
        return self.aslist() == other

    def __iter__(self):
        return iter([self.left, self.right])

    def __mul__(self, other):
        return (3 * self.left + 2 * self.right) * other

    def __rmul__(self, other):
        return other * (3 * self.left + 2 * self.right)


def reduce(number: Pair) -> Pair:
    try:
        again = True
        print("start reduce", number)
        while again:
            again = False
            print(number)
            if number.checkExplode():
                again = True
                continue
            if number.split():
                again = True
                continue
        print("end reduce", number)
        return number
    except:
        print("error:", number)
        raise


def add(numberLeft: Pair, numberRight: Pair) -> Pair:
    print("start add", numberLeft, numberRight)
    return reduce(Pair([numberLeft, numberRight]))


def magnitude(number: Pair) -> int:
    left, right = number
    if type(left) is Pair:
        left = magnitude(left)
    if type(right) is Pair:
        right = magnitude(right)
    return 3 * left + 2 * right


def parse(value: str) -> Pair:
    base = loads(value)
    return Pair(base)


def solve18(values: str):
    res = None
    for line in values.splitlines():
        if not res:
            res = parse(line)
        else:
            res = add(res, parse(line))
    return magnitude(res)


def solve18_2(values):
    res = 0
    for x, y in permutations(values.splitlines(), 2):
        res = max(res, magnitude(add(parse(x), parse(y))))
    return res


if __name__ == "__main__":
    main()
