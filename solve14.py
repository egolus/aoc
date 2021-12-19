#!/bin/env python
from itertools import groupby, pairwise
from aocd import get_data, submit
from pprint import pprint


def main():
    values = get_data(day=14, year=2021).split("\n")
    testvalues = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".split("\n")
    testtrue = 1588
    testtrue_b = 2188189693529

    testresult = solve14(testvalues, 10)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve14(values, 10)
    print("solve14:", result)

    # input("submit?")
    submit(result, part="a", day=14, year=2021)

    testresult_b = solve14_b(testvalues, 10)
    assert testresult_b == testtrue, f"{testresult_b} != {testtrue}"
    testresult2_b = solve14_b(testvalues, 40)
    assert testresult2_b == testtrue_b, f"{testresult2_b} != {testtrue_b}"
    result_b = solve14_b(values, 40)
    print("solve14_b:", result_b)

    # input("submit?")
    submit(result_b, part="b", day=14, year=2021)


def solve14(values, steps):
    result = 0
    template = values[0]
    rules = {}
    for rule in values[2:]:
        k, v = rule.split(" -> ")
        rules[k] = v
    print(template, rules)
    for step in range(steps):
        newTemp = ""
        for c in template:
            if newTemp:
                newTemp += rules[newTemp[-1] + c]
            newTemp += c
        template = newTemp
        counts = {}
        for k, g in groupby(sorted(newTemp)):
            counts[k] = len(list(g))
        maxK = sorted(counts.items(), key=lambda kv: kv[1])[-1]
        minK = sorted(counts.items(), key=lambda kv: kv[1])[0]
        print(minK, maxK)
    return maxK[1] - minK[1]


def solve14_b(values, steps):
    result = 0
    template = values[0]
    rules = {}
    for rule in values[2:]:
        k, v = rule.split(" -> ")
        rules[k] = v
    print(template, rules)
    counts = {}
    for key in rules:
        counts[key] = 0
    for x, y in pairwise(template):
        counts[x+y] += 1
    pprint({k:v for k, v in counts.items() if v > 0})
    for step in range(steps):
        newCounts = {}
        for key in rules:
            newCounts[key] = 0
        for key, val in counts.items():
            newCounts[key[0] + rules[key]] += val
            newCounts[rules[key] + key[1]] += val
        pprint({k:v for k, v in newCounts.items() if v > 0})
        keyCounts = {}
        for k, v in newCounts.items():
            if k[0] in keyCounts:
                keyCounts[k[0]] += v
            else:
                keyCounts[k[0]] = v
        keyCounts[template[-1]] += 1
        maxK = sorted(keyCounts.items(), key=lambda kv: kv[1])[-1]
        minK = sorted(keyCounts.items(), key=lambda kv: kv[1])[0]
        print(sorted(keyCounts.items(), key=lambda kv: kv[1]), maxK, minK)
        counts = newCounts

    return maxK[1] - minK[1]

if __name__ == "__main__":
    main()
