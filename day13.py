import pytest
import math
import re
from helpers import load_lines

# partA simple,
# partB the OFFSET makes in too timeconsuming for a simple iteration
OFFSET = 10000000000000


def parse_data(fname):
    "returns a list [((ax,ay),(bx,by),(px,py))...]"
    result = []
    a, b, p = None, None, None
    pattern = re.compile(r"^(.*): X.(.*), Y.(.*)$")
    for line in load_lines(fname):
        m = pattern.search(line)
        if m is None:
            continue
        if m.group(1) == "Button A":
            a = (int(m.group(2)), int(m.group(3)))
        elif m.group(1) == "Button B":
            b = (int(m.group(2)), int(m.group(3)))
        elif m.group(1) == "Prize":
            p = (int(m.group(2)), int(m.group(3)))
            result.append((a, b, p))
    return result


def calc_pressed(a, b, p):
    """given a,b&p resturn a list [(pa,pb)...] of all possible combinations
    which give the prize."""
    ax, ay = a
    bx, by = b
    px, py = p
    result = []
    # Simplest method that works:brute force, all amounts of A presses
    for pa in range(0, px // ax):
        pb = (px - (pa * ax)) // bx
        # pa,pb are estimated presses, see if its possible
        if pb >= 0 and pa * ax + pb * bx == px and pa * ay + pb * by == py:
            result.append((pa, pb))
    return result


def day13a(fname):
    data = parse_data(fname)
    total = 0
    for d in data:
        presses = calc_pressed(d[0], d[1], d[2])
        scores = [pa * 3 + pb for pa, pb in presses]
        if len(scores) > 0:
            total += min(scores)
    return total


def calc_pressed_b(a, b, p):
    """given a,b&p resturn a list [(pa,pb)...] of all possible combinations
    which give the prize."""
    ax, ay = a
    bx, by = b
    px, py = p
    result = []
    # going for twin simultanous equation method
    # pa*ax+pb*bx==px and pa*ay+pb*by==py where pa,pb are the unknowns
    # ax+by=c dx+ey=f (simplest form)
    # aex+bey=ce, bdx+bey=bf (cross multiply)
    # aex-bdx=ce-bf (substract)
    # x=(ce-bf)/(ae-bd) y=(c-ax)/b (solve & substitute)
    pa = (px * by - bx * py) / (ax * by - bx * ay)
    pb = (px - ax * pa) / bx
    ##    print("pa,pb",pa,pb)
    if (
        pa == int(pa)
        and pb == int(pb)
        and pa >= 0
        and pb >= 0
        and pa * ax + pb * bx == px
        and pa * ay + pb * by == py
    ):
        result.append((int(pa), int(pb)))
    return result


def day13b(fname):
    data = parse_data(fname)
    total = 0
    for d in data:
        px, py = OFFSET + d[2][0], OFFSET + d[2][1]
        presses = calc_pressed_b(d[0], d[1], (px, py))
        scores = [pa * 3 + pb for pa, pb in presses]
        if len(scores) > 0:
            total += min(scores)
    return total


################################################################
if __name__ == "__main__":
    print("day13a", day13a("input13.txt"))
    print("day13b", day13b("input13.txt"))

################################################################


def test_parse_data():
    result = parse_data("test13.txt")
    assert len(result) == 4
    assert result[0] == ((94, 34), (22, 67), (8400, 5400))
    assert result[-1] == ((69, 23), (27, 71), (18641, 10279))


def test_calc_pressed():
    data = parse_data("test13.txt")
    calc = lambda d: calc_pressed(d[0], d[1], d[2])
    assert calc(data[0]) == [(80, 40)]
    assert calc(data[1]) == []
    assert calc(data[2]) == [(38, 86)]
    assert calc(data[3]) == []


def test_day13a():
    assert day13a("test13.txt") == 480


def test_calc_pressed_b():
    data = parse_data("test13.txt")

    calc = lambda d: calc_pressed_b(d[0], d[1], d[2])
    calc_offset = lambda d: calc_pressed_b(
        d[0], d[1], (OFFSET + d[2][0], OFFSET + d[2][1])
    )
    # make sure it works
    assert calc(data[0]) == [(80, 40)]
    assert calc(data[1]) == []
    assert calc(data[2]) == [(38, 86)]
    assert calc(data[3]) == []

    # check offset works
    # question didn't give the numbers, so just looking for possible/not
    assert calc_offset(data[0]) == []
    assert len(calc_offset(data[1])) > 0
    assert calc_offset(data[2]) == []
    assert len(calc_offset(data[3])) > 0
