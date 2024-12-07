import pytest
import re
from helpers import load_tokens

# This was getting a bit slow on the part B


def parse_data(fname):
    "returns [(val,[])]"
    result = []
    for line in load_tokens(fname):
        val = int(line[0][:-1])  # chop the left char ':'
        arr = [int(val) for val in line[1:]]
        result.append((val, arr))
    return result


def day07a(fname):
    data = parse_data(fname)
    score = 0
    for val, arr in data:
        ln = len(arr)
        match = False
        # for 2 numbers is arr[0]+arr[1] or *
        # for 3 is 0+1+2, 0*1+2, 0+1*2, 0*1*2
        for i in range(2 ** (ln - 1)):  # 2^ln if all possible options
            num = arr[0]
            # print(num,end=' ')
            # for each number:
            for n in range(1, ln):
                if i % 2 == 0:
                    # print("+",arr[n],end=' ')
                    num += arr[n]
                else:
                    # print("*",arr[n],end=' ')
                    num *= arr[n]
                i //= 2
            # print("=",num)
            if num == val:
                match = True
                break
        if match:
            score += val

    return score


def concat(a, b):
    "returns a||b"
    # return int(str(a)+str(b))
    t = b
    while t > 0:
        t //= 10
        a *= 10
    return a + b


def day07b(fname):
    data = parse_data(fname)
    score = 0
    for val, arr in data:
        ln = len(arr)
        match = False

        for i in range(3 ** (ln - 1)):  # 3^ln if all possible options
            num = arr[0]
            for n in range(1, ln):
                if i % 3 == 0:
                    num += arr[n]
                elif i % 3 == 1:
                    num *= arr[n]
                else:
                    # what fun! 123||456=123456
                    num = concat(num, arr[n])

                i //= 3
            # print("=",num)
            if num == val:
                match = True
                break
        if match:
            score += val

    return score


################################################################
if __name__ == "__main__":
    print("day07a", day07a("input07.txt"))
    print("day07b", day07b("input07.txt"))

################################################################


def test_parse_data():
    data = parse_data("test07.txt")
    assert len(data) == 9
    assert data[0] == (190, [10, 19])
    assert data[-1] == (292, [11, 6, 16, 20])


def test_day07a():
    assert day07a("test07.txt") == 3749


def test_day07b():
    assert day07b("test07.txt") == 11387
