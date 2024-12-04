import pytest
import re
from helpers import load_file


def day03a(fname):
    line = load_file(fname)
    matches = re.findall(r"mul\((\d+),(\d+)\)", line)
    return sum(int(m[0]) * int(m[1]) for m in matches)


def day03b(fname):
    line = load_file(fname)
    total = 0
    do = True
    regex = re.compile(r"mul\((\d+),(\d+)\)")
    for l in re.split(r"(do\(\)|don\'t\(\))", line):
        if l == "do()":
            do = True
        elif l == "don't()":
            do = False
        else:
            if do:
                matches = regex.findall(l)
                total += sum(int(m[0]) * int(m[1]) for m in matches)

    return total


################################################################
if __name__ == "__main__":
    print("day03a", day03a("input03.txt"))
    print("day03b", day03b("input03.txt"))

################################################################


def test_day03a():
    assert day03a("test03.txt") == 161


def test_day03b():
    assert day03b("test03b.txt") == 48
