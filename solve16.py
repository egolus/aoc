#!/bin/env python
from itertools import tee, product
from aocd import get_data, submit
from pprint import pprint


bits = {
    "0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100",
    "5": "0101", "6": "0110", "7": "0111", "8": "1000", "9": "1001",
    "A": "1010", "B": "1011", "C": "1100", "D": "1101", "E": "1110",
    "F": "1111",
}
dec = {
    "0000": "0", "0001": "1", "0010": "2", "0011": "3", "0100": "4",
    "0101": "5", "0110": "6", "0111": "7", "1000": "8", "1001": "9",
    "1010": "A", "1011": "B", "1100": "C", "1101": "D", "1110": "E",
    "1111": "F",
}


def main():
    values = get_data(day=16, year=2021)
    testvalues1 = "110100101111111000101000"
    testtrue1 = (6, 4, "011111100101")
    testvalues2 = "00111000000000000110111101000101001010010001001000000000"
    testtrue2 = (1, 6, [(6, 4, "1010"), (2, 4, "00010100")])
    testvalues3 = "11101110000000001101010000001100100000100011000001100000"
    testtrue3 = (7, 3, [(2, 4, "0001"), (4, 4, "0010"), (1, 4, "0011")])
    testvalues4 = "8A004A801A8002F478"
    testtrue4 = 16
    testvalues5 = "620080001611562C8802118E34"
    testtrue5 = 12

    testvalues6 = "C200B40A82"
    testtrue6 = 3
    testvalues7 = "04005AC33890"
    testtrue7 = 54

    testresult1 = next(getPacket(testvalues1))
    assert testresult1 == testtrue1, f"{testresult1} != {testtrue1}"
    testresult2 = next(getPacket(testvalues2))
    assert testresult2 == testtrue2, f"{testresult2} != {testtrue2}"
    testresult3 = next(getPacket(testvalues3))
    assert testresult3 == testtrue3, f"{testresult3} != {testtrue3}"

    testresult4 = solve16(testvalues4)
    assert testresult4 == testtrue4, f"{testresult4} != {testtrue4}"
    testresult5 = solve16(testvalues5)
    assert testresult5 == testtrue5, f"{testresult5} != {testtrue5}"

    result = solve16(values)
    print("solve16:", result)

    testresult6 = solve16_2(testvalues6)
    assert testresult6 == testtrue6, f"{testresult6} != {testtrue6}"
    testresult7 = solve16_2(testvalues7)
    assert testresult7 == testtrue7, f"{testresult7} != {testtrue7}"

    # input("submit?")
    submit(result, part="a", day=16, year=2021)

    result2 = solve16_2(values)
    print("solve16_2:", result2)

    # input("submit?")
    submit(result2, part="b", day=16, year=2021)


def getPacket(bits):
    if type(bits) is str:
        biter = iter(bits)
    else:
        biter = bits
    while True:
        try:
            header = -1
            pid = -1
            groups = []
            head = []
            _pid = []
            for _ in range(3):
                head += next(biter)
            header = int("".join(head), 2)
            for _ in range(3):
                _pid += next(biter)
            pid = int("".join(_pid), 2)

            if pid == 4:
                print("literal")
                # literal value packet
                while biter:
                    group = []
                    for _ in range(5):
                        group += next(biter)
                    groups.append(group)
                    if group[0] == "0":
                        # try:
                            # while next(biter) == "0":
                                # pass
                        # except StopIteration:
                            # pass
                        print("packet:", (header, pid, "".join(["".join(g[1:]) for g in groups])))
                        yield (header, pid, "".join(["".join(g[1:]) for g in groups]))
                        break

            else:
                print("operator")
                # operator packet
                i = next(biter)
                if i == '0':
                    blen = 15
                    print(blen)
                    plength = []
                    for _ in range(blen):
                        plength += next(biter)
                    print("".join(plength))
                    subs = []
                    for _ in range(int("".join(plength), 2)):
                        subs += next(biter)
                    print("subs:", "".join(subs))
                    subpackets = [packet for packet in getPacket(iter("".join(subs)))]
                    print("packet:", (header, pid, subpackets))
                    yield (header, pid, subpackets)
                else:
                    blen = 11
                    plength = []
                    for _ in range(blen):
                        plength += next(biter)
                    print("".join(plength))
                    subpackets = []
                    for _ in range(int("".join(plength), 2)):
                        subpackets.append(next(getPacket(biter)))
                    print("packet:", (header, pid, subpackets))
                    yield (header, pid, subpackets)
        except StopIteration:
            print("stop")
            return


def getPacketHeaders(packet, lst):
    lst.append(packet[0])
    if packet[1] == 4:
        print(packet)
    else:
        for p in (getPacketHeaders(sub, lst) for sub in packet[2]):
            print(p)


def interpretPackets(packet):
    print(packet)
    head, pid, rest = packet
    if pid == 0:
        # sum
        if len(rest) == 1:
            return interpretPackets(rest[0])
        else:
            return sum(interpretPackets(p) for p in rest)
    if pid == 1:
        if len(rest) == 1:
            return interpretPackets(rest[0])
        else:
            ps = [interpretPackets(p) for p in rest]
            res = ps[0]
            for p in ps[1:]:
                res = res * p
            return res
    if pid == 2:
        return min(interpretPackets(p) for p in rest)
    if pid == 3:
        return max(interpretPackets(p) for p in rest)
    if pid == 4:
        return int(rest, 2)
    if pid == 5:
        return 1 if interpretPackets(rest[0]) > interpretPackets(rest[1]) else 0
    if pid == 6:
        return 1 if interpretPackets(rest[0]) < interpretPackets(rest[1]) else 0
    if pid == 7:
        return 1 if interpretPackets(rest[0]) == interpretPackets(rest[1]) else 0


def solve16(values):
    biits = "".join([bits[c] for c in values])
    packets = getPacket(biits)
    lst = []
    for packet in packets:
        getPacketHeaders(packet, lst)
    print(lst)
    return sum(int(h) for h in lst)


def solve16_2(values):
    biits = "".join([bits[c] for c in values])
    packets = getPacket(biits)
    return interpretPackets(next(packets))


if __name__ == "__main__":
    main()
