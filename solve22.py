#!/bin/env python
from aocd import get_data, submit


def main():
    values = get_data(day=22, year=2021)
    testvalues = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""
    testvalues2 = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""
    testtrue = 39
    testtrue2 = 590784

    testresult = solve22(testvalues)
    print("testresult:", testresult)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    testresult2 = solve22(testvalues2)
    print("testresult2:", testresult2)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"

    result = solve22(values)
    print("solve22:", result)

    # input("submit?")
    submit(result, part="a", day=22, year=2021)

    testvalues_2 = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29"""

    testtrue_2 = 2758514936282235

    testresult_2 = solve22_2(testvalues_2)
    assert testresult_2 == testtrue_2, f"{testresult_2} != {testtrue_2}"

    return
    result2 = solve22_2(values)
    print("solve22_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=22, year=2021)


def solve22(values):
    cubes = {}
    for line in values.splitlines():
        switch, coords = line.split(" ")
        xs, ys, zs = coords.split(",")
        xs = [int(i) for i in xs.removeprefix("x=").split("..")]
        ys = [int(i) for i in ys.removeprefix("y=").split("..")]
        zs = [int(i) for i in zs.removeprefix("z=").split("..")]
        print(xs, ys, zs)
        if xs[0] < -50:
            xs[0] = -50
        if xs[1] > 50:
            xs[1] = 50
        if ys[0] < -50:
            ys[0] = -50
        if ys[1] > 50:
            ys[1] = 50
        if zs[0] < -50:
            zs[0] = -50
        if zs[1] > 50:
            zs[1] = 50
        if (((xs[0] < 51) and (-51 < xs[1])) and
                ((ys[0] < 51) and (-51 < ys[1])) and
                ((zs[0] < 51) and (-51 < zs[1]))):
            print(xs, ys, zs)
            for x in range(xs[0], xs[1] + 1):
                for y in range(ys[0], ys[1] + 1):
                    for z in range(zs[0], zs[1] + 1):
                        if switch == "on":
                            cubes[(x, y, z)] = 1
                        else:
                            cubes.pop((x, y, z), None)
        else:
            print("skip")
    return len(cubes)


def removeCubes(cubes, remover):
    rxs, rys, rzs = remover
    for cube in cubes:
        xs, ys, zs = cube
        if (
                ((xs[0] < rxs[0] < xs[1]) or
                    (xs[0] < rxs[1] < xs[1]) or
                    (rxs[0] < xs[1] and xs[0] < rxs[1])) and
                ((ys[0] < rys[0] < ys[1]) or
                    (ys[0] < rys[1] < ys[1]) or
                    (rys[0] < ys[1] and ys[0] < rys[1])) and
                ((zs[0] < rzs[0] < zs[1]) or
                    (zs[0] < rzs[1] < zs[1]) or
                    (rzs[0] < zs[1] and zs[0] < rzs[1]))
                ):
            cubes.remove(cube)


def solve22_2(values):
    cubes = []
    for line in values.splitlines():
        switch, coords = line.split(" ")
        switch = True if switch == "on" else False
        xs, ys, zs = coords.split(",")
        xs = [int(i) for i in xs.removeprefix("x=").split("..")]
        ys = [int(i) for i in ys.removeprefix("y=").split("..")]
        zs = [int(i) for i in zs.removeprefix("z=").split("..")]
        print(xs, ys, zs)
        if switch:
            cubes.append((xs, ys, zs))
        else:
            removeCubes(cubes, (xs, ys, zs))


if __name__ == "__main__":
    main()
