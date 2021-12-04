#!/bin/env python

with open("../input03", "r") as infile:
    lines = list(x.strip() for x in infile.readlines())


def solve03():
    gamma = ""
    epsilon = ""
    for i in range(len(lines[0])):
        bit = 0
        for line in lines:
            bit += int(line[i])
        bit = round(bit / len(lines))
        gamma += str(bit)
        epsilon += str(int(not bit))
    # print(f"gamma: {gamma}, epsilon: {epsilon}")
    return (int(gamma, 2) * int(epsilon, 2))


def solve03_2():
    oxy = ""
    co2 = ""
    filtered = lines.copy()
    for i in range(len(lines[0])):
        bit = 0
        for line in filtered:
            bit += int(line[i])
        bit = int(bit >= (len(filtered) / 2))
        filtered = [line for line in filtered if line[i] == str(bit)]
        # print(f"bit: {bit}, len(filtered): {len(filtered)}")
        if len(filtered) == 1:
            oxy = filtered[0]
            break

    filtered = lines.copy()
    for i in range(len(lines[0])):
        bit = 0
        for line in filtered:
            bit += int(line[i])
        bit = int(bit >= (len(filtered) / 2))
        filtered = [line for line in filtered if line[i] != str(bit)]
        # print(f"bit: {bit}, len(filtered): {len(filtered)}")
        if len(filtered) == 1:
            co2 = filtered[0]
    # print(f"oxy: {oxy}|{int(oxy, 2)}, co2: {co2}|{int(co2, 2)}")
    return (int(oxy, 2) * int(co2, 2))


if __name__ == "__main__":
    print("solve03:", solve03())
    print("solve03_2:", solve03_2())
