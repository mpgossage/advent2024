import pytest
import math
from helpers import load_file

# This is a classic AOC puzzle:
# given is a pattern,
# part A: after X cycles it gives what?
# part B: after a gazillion cycles it gives what?
# Its looking like it can be easily solved using memorisation, lets find out
# quick test proves brute force will not work, it dies ~35 blinks


def blink(line):
    "returns the modified line"
    result = []
    for l in line:
        strl = str(l)
        if l == 0:
            result.append(1)
        elif len(strl) % 2 == 0:
            halfln = len(strl) // 2
            result.append(int(strl[:halfln]))
            result.append(int(strl[halfln:]))
        else:
            result.append(l * 2024)
    return result


def multiblink(line, times):
    "given line, blink a number of times, return the number of stones"
    for i in range(times):
        line = blink(line)
    return len(line)


def day11a(fname):
    data = [int(a) for a in load_file(fname).strip("\n").split()]
    return multiblink(data, 25)


def multiblink_b(line, times):
    """optimised version using dynamic programming/caching.
    key feature we can exploit: stones do not effect their neighbour.
    If I know that a stone value X will become Y stones after 5 blinks,
    then I can cache this and look it up always.
    I also can look at each stone on its own."""

    def _blink(stone, times, cache):
        lookup = cache.get((stone, times))
        if lookup is not None:
            return lookup
        # if its one time, do the blink & store the result
        if times == 1:
            result = len(blink([stone]))
            cache[(stone, times)] = result
            return result
        # if its more than one: blink & lookup each new stone
        result = 0
        newstones = blink([stone])
        for ns in newstones:
            result += _blink(ns, times - 1, cache)
        # add to the cache
        cache[(stone, times)] = result
        return result

    cache = {}
    result = 0
    for l in line:
        result += _blink(l, times, cache)
    return result


def day11b(fname):
    ##    "stupid version"
    ##    data=[int(a) for a in load_file(fname).strip("\n").split()]
    ##    return multiblink(data,75)

    data = [int(a) for a in load_file(fname).strip("\n").split()]
    return multiblink_b(data, 75)


################################################################
if __name__ == "__main__":
    print("day11a", day11a("input11.txt"))
    print("day11b", day11b("input11.txt"))

################################################################


def test_blink1():
    assert blink([0, 1, 10, 99, 999]) == [1, 2024, 1, 0, 9, 9, 2021976]


def test_blink2():
    assert blink([125, 17]) == [253000, 1, 7]


def test_multiblink():
    data = [125, 17]
    assert multiblink(data, 1) == 3
    assert multiblink(data, 2) == 4
    assert multiblink(data, 3) == 5
    assert multiblink(data, 4) == 9
    assert multiblink(data, 5) == 13
    assert multiblink(data, 6) == 22
    assert multiblink(data, 25) == 55312


def test_day11a():
    assert day11a("test11.txt")


def test_multiblink_b_1():
    assert multiblink_b([0], 1) == 1
    assert multiblink_b([1], 1) == 1
    assert multiblink_b([10], 1) == 2
    assert multiblink_b([99], 1) == 2
    assert multiblink_b([999], 1) == 1
    assert multiblink_b([0, 1, 10, 99, 999], 1) == 7


def test_multiblink_b_2():
    data = [125, 17]
    assert multiblink_b(data, 1) == 3
    assert multiblink_b(data, 2) == 4
    assert multiblink_b(data, 3) == 5
    assert multiblink_b(data, 4) == 9
    assert multiblink_b(data, 5) == 13
    assert multiblink_b(data, 6) == 22
    assert multiblink_b(data, 25) == 55312
