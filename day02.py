import pytest
from helpers import load_int_tokens


def parse_input(fname):
    results = []
    with open(fname) as f:
        t = []
        for line in f:
            line = line.strip()
            if len(line) == 0:
                results.append(t)
                t = []
            else:
                t.append(int(line))
        results.append(t)
    return results


def safe_line(line):
    # if all values should be decreasing
    dec = line[0] > line[1]
    for i in range(len(line) - 1):
        delta = line[i + 1] - line[i]
        if dec:
            if -3 <= delta <= -1:
                pass
            else:
                return False
        else:
            if 3 >= delta >= 1:
                pass
            else:
                return False
    return True


def day02a(fname):
    lines = load_int_tokens(fname)
    return sum(1 for l in lines if safe_line(l))


def safe_line_less_one(line):
    if safe_line(line):
        return True
    # remove one at a time & see if any are safe
    for i in range(len(line)):
        l = line[:i] + line[i + 1 :]
        if safe_line(l):
            return True
    return False


def day02b(fname):
    lines = load_int_tokens(fname)
    return sum(1 for l in lines if safe_line_less_one(l))


################################################################
if __name__ == "__main__":
    ##    print(load_int_tokens("test02.txt"))
    print("day02a", day02a("input02.txt"))
    print("day02b", day02b("input02.txt"))

################################################################


def test_parse():
    results = load_int_tokens("test02.txt")
    assert len(results) == 6
    assert results[0] == [7, 6, 4, 2, 1]
    assert results[-1] == [1, 3, 6, 7, 9]


def test_day02a():
    assert day02a("test02.txt") == 2


def test_day01b():
    assert day02b("test02.txt") == 4
