#!/bin/env python
from aocd import get_data, submit
from pprint import pprint


low = "abcdefghijklmnopqrstuvwxyz"


def main():
    values = get_data(day=12, year=2021).split("\n")
    testvalues1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end""".split("\n")
    testvalues2 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".split("\n")
    testtrue1 = 10
    testtrue2 = 226
    testtrue1b = 36
    testtrue2b = 3509

    testresult1 = solve12(testvalues1)
    assert testresult1 == testtrue1, f"{testresult1} != {testtrue1}"
    testresult2 = solve12(testvalues2)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result = solve12(values)
    print("solve12:", result)

    # input("submit?")
    submit(result, part="a", day=12, year=2021)

    testresult1b = solve12_2(testvalues1)
    assert testresult1b == testtrue1b, f"{testresult1b} != {testtrue1b}"
    testresult2b = solve12_2(testvalues2)
    assert testresult2b == testtrue2b, f"{testresult2b} != {testtrue2b}"
    result2 = solve12_2(values)
    print("solve12_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=12, year=2021)


def traverse(node, nodes, visited, again=False):
    paths = []

    if node[0] in low:
        visited.append(node)
    for other in nodes[node]:
        if other == "start":
            continue
        if other == "end":
            paths.append([node, "end"])
        elif other[0] not in low:
            res = traverse(other, nodes, [x for x in visited], again=again)
            for path in res:
                paths.append([node] + path)
        elif (other[0] in low) and (other not in visited):
            if other in visited:
                again = False
            res = traverse(other, nodes, [x for x in visited], again=again)
            for path in res:
                paths += [[node] + path]
        elif (other[0] in low) and again:
            if len([x for x in visited if x == other]) < 2:
                res = traverse(other, nodes, [x for x in visited], again=False)
                for path in res:
                    paths += [[node] + path]

    return paths


def solve12(lines):
    nodes = {}
    paths = []
    for line in lines:
        node1, node2 = line.split("-")
        if node1 in nodes:
            nodes[node1].append(node2)
        else:
            nodes[node1] = [node2]
        if node2 in nodes:
            nodes[node2].append(node1)
        else:
            nodes[node2] = [node1]
    pprint(nodes)

    res = traverse("start", nodes, [])
    for path in res:
        paths.append(path)
    # for node, others in nodes.items():
        # res = traverse(node, others)
        # paths.append([node].append(res))
    print()
    pprint([",".join(path) for path in paths])
    return len(paths)


def solve12_2(lines):
    nodes = {}
    paths = []
    for line in lines:
        node1, node2 = line.split("-")
        if node1 in nodes:
            nodes[node1].append(node2)
        else:
            nodes[node1] = [node2]
        if node2 in nodes:
            nodes[node2].append(node1)
        else:
            nodes[node2] = [node1]
    pprint(nodes)

    res = traverse("start", nodes, [], again=True)
    for path in res:
        paths.append(path)
    # for node, others in nodes.items():
        # res = traverse(node, others)
        # paths.append([node].append(res))
    print()
    pprint([",".join(path) for path in paths])
    return len(paths)


if __name__ == "__main__":
    main()
