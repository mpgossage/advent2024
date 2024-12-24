import pytest
import math
from helpers import load_lines

""" Part A assumed brute force would work.
It does on test, but not the real thing.
Added the simple caching it flies, parts A&B"""


def parse_data(fname):
    "returns [tokens],[patterns]"
    lines = load_lines(fname)
    tokens = [t.strip() for t in lines[0].split(",")]
    patterns = lines[2:]
    return tokens, patterns


def towel_pattern(tokens, pattern):
    "returns true if it can be made"
    # simple recursive solution
    if pattern == "":
        return True
    for t in tokens:
        if pattern.startswith(t):
            if towel_pattern(tokens, pattern[len(t) :]):
                return True
    return False


def towel_pattern2(tokens, pattern, cache):
    "returns true if it can be made"
    # simple recursive solution
    if pattern in cache:
        return cache[pattern]
    for t in tokens:
        if pattern.startswith(t):
            if towel_pattern2(tokens, pattern[len(t) :], cache):
                cache[pattern] = True
                return True
    cache[pattern] = False
    return False


def towel_pattern_count(tokens, pattern, cache):
    "returns number of ways that pattern can be made (0 for error)"
    # simple recursive solution
    if pattern in cache:
        return cache[pattern]
    count = 0
    for t in tokens:
        if pattern.startswith(t):
            count += towel_pattern_count(tokens, pattern[len(t) :], cache)
    cache[pattern] = count
    return count


def day19a(fname):
    tokens, patterns = parse_data(fname)
    result = 0
    cache = {"": True}
    for p in patterns:
        if towel_pattern2(tokens, p, cache):
            result += 1
        print(p)
    return result


def day19b(fname):
    tokens, patterns = parse_data(fname)
    result = 0
    cache = {"": 1}
    for p in patterns:
        result += towel_pattern_count(tokens, p, cache)
    return result


################################################################
if __name__ == "__main__":
    print("day19a", day19a("input19.txt"))
    print("day19b", day19b("input19.txt"))


################################################################


def test_parse_data():
    tokens, patterns = parse_data("test19.txt")
    assert len(tokens) == 8
    assert tokens[0] == "r"
    assert tokens[-1] == "br"
    assert len(patterns) == 8
    assert patterns[0] == "brwrr"
    assert patterns[-1] == "bbrgwb"


def test_towel_patten():
    tokens, patterns = parse_data("test19.txt")
    assert towel_pattern(tokens, patterns[0])
    assert towel_pattern(tokens, patterns[4]) == False
    assert towel_pattern(tokens, patterns[5])
    assert towel_pattern(tokens, patterns[-1]) == False


def test_day19a():
    assert day19a("test19.txt") == 6


def test_towel_patten2():
    tokens, patterns = parse_data("test19.txt")
    cache = {"": True}
    assert towel_pattern2(tokens, patterns[0], cache)
    assert towel_pattern2(tokens, patterns[4], cache) == False
    assert towel_pattern2(tokens, patterns[5], cache)
    assert towel_pattern2(tokens, patterns[-1], cache) == False


def test_towel_patten_count():
    tokens, patterns = parse_data("test19.txt")
    cache = {"": 1}
    assert towel_pattern_count(tokens, patterns[0], cache) == 2
    assert towel_pattern_count(tokens, patterns[2], cache) == 4
    assert towel_pattern_count(tokens, patterns[4], cache) == 0
    assert towel_pattern_count(tokens, patterns[-1], cache) == 0


def test_day19b():
    assert day19b("test19.txt") == 16
