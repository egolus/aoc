#!/bin/env python
from aocd import get_data, submit
from pprint import pprint


def main():
    values = get_data(day=20, year=2021)
    testvalues = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
    testtrue = 35
    testtrue2 = 3351

    testresult = solve20(testvalues)
    assert testresult == testtrue, f"{testresult} != {testtrue}"
    result = solve20(values)
    print("solve20:", result)

    # input("submit?")
    # submit(result, part="a", day=20, year=2021)

    testresult2 = solve20(testvalues, 50)
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    result2 = solve20(values, 50)
    print("solve20_2:", result2)

    # input("submit?")
    # submit(result2, part="b", day=20, year=2021)


def enhancePixel(pixel, image, enhancer):
    pixel
    searchspace = [[0,0,0], [0,0,0], [0,0,0]]
    maxX = len(image[0]) - 1
    maxY = len(image) - 1
    if pixel[0] > 0 and pixel[1] > 0:
        searchspace[0][0] = image[pixel[1] - 1][pixel[0] - 1]
    if pixel[1] > 0:
        searchspace[0][1] = image[pixel[1] - 1][pixel[0]]
    if pixel[0] < maxX and pixel[1] > 0:
        searchspace[0][2] = image[pixel[1] - 1][pixel[0] + 1]
    if pixel[0] > 0:
        searchspace[1][0] = image[pixel[1]][pixel[0] - 1]
    searchspace[1][1] = image[pixel[1]][pixel[0]]
    if pixel[0] < maxX:
        searchspace[1][2] = image[pixel[1]][pixel[0] + 1]
    if pixel[0] > 0 and pixel[1] < maxY:
        searchspace[2][0] = image[pixel[1] + 1][pixel[0] - 1]
    if pixel[1] < maxY:
        searchspace[2][1] = image[pixel[1] + 1][pixel[0]]
    if pixel[0] < maxX and pixel[1] < maxY:
        searchspace[2][2] = image[pixel[1] + 1][pixel[0] + 1]
    binary = "".join([str(x) for line in searchspace for x in line])
    return enhancer[int(binary, 2)]


def printImage(image):
    for line in image:
        for p in line:
            print("#" if p else ".", end="")
        print()
    print()


def solve20(values, rounds=2):
    lines = values.splitlines()
    enhancer = [1 if x == "#" else 0 for x in lines[0]]
    image = []
    for line in lines[2:]:
        image.append([1 if x == "#" else 0 for x in line])
    print(enhancer)
    for _ in range(rounds * 2):
        for y in range(len(image)):
            image[y] = [0] + image[y] + [0]
        image = [[0 for x in range(len(image[0]))]] \
            + image + \
            [[0 for x in range(len(image[0]))]]
    for _ in range(rounds):
        newImage = []
        printImage(image)
        for y in range(len(image)):
            line = []
            for x in range(len(image[0])):
                line.append(enhancePixel((x, y), image, enhancer))
            newImage.append(line)
        printImage(newImage)
        image = newImage
    image = image[rounds:-rounds]
    for y in range(len(image)):
        image[y] = image[y][rounds:-rounds]
    printImage(image)
    return sum(sum(image[y]) for y in range(len(image)))


if __name__ == "__main__":
    main()
