import pytest
from helpers import load_tokens


def parse_input(fname):
    l1, l2 = [], []
    for l in load_tokens(fname):
        l1.append(int(l[0]))
        l2.append(int(l[1]))
    return l1, l2


def day01a(fname):
    a, b = parse_input(fname)
    # sort and compare
    a.sort()
    b.sort()
    total = 0
    for i in range(len(a)):
        total += abs(a[i] - b[i])
    return total


def day01b(fname):
    a, b = parse_input(fname)
    total = 0
    for v in a:
        total += v * b.count(v)
    return total


################################################################
if __name__ == "__main__":
    ##    print(parse_input("test01.txt"))
    print("day01a", day01a("input01.txt"))
    print("day01b", day01b("input01.txt"))

################################################################


def test_parse():
    a, b = parse_input("test01.txt")
    assert len(a) == 6
    assert len(b) == 6
    assert a == [3, 4, 2, 1, 3, 3]
    assert b == [4, 3, 5, 3, 9, 3]


def test_day01a():
    assert day01a("test01.txt") == 11


def test_day01b():
    assert day01b("test01.txt") == 31
