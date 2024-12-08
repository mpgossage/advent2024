import pytest
import math
from helpers import load_lines

# This is jolly confusing, the antinode computation routine
# is going to need a lot of test cases so I can understand what it means.
# Update, it makes sense now, I'm thick.


def parse_data(fname):
    "returns (sx,sy),{A:[(x0,y0),(x1,y1)...]}"
    data = load_lines(fname)
    size = (len(data[0]), len(data))
    nodes = {}

    for y, line in enumerate(data):
        for x, ch in enumerate(line):
            if ch == ".":
                continue
            if ch in nodes:
                nodes[ch].append((x, y))
            else:
                nodes[ch] = [(x, y)]

    return size, nodes


def find_antinodes(size, nodes):
    "if A & B are nodes, then B+(B-A) & A-(B-A) are antinodes"

    result = {}
    for n, nlist in nodes.items():
        ln = len(nlist)
        an = set()
        # foreach node pair
        for i in range(ln - 1):
            for j in range(i + 1, ln):
                na, nb = nlist[i], nlist[j]
                dx, dy = nb[0] - na[0], nb[1] - na[1]
                p1 = (nb[0] + dx, nb[1] + dy)
                p2 = (na[0] - dx, na[1] - dy)
                if 0 <= p1[0] < size[0] and 0 <= p1[1] < size[1]:
                    an.add(p1)
                if 0 <= p2[0] < size[0] and 0 <= p2[1] < size[1]:
                    an.add(p2)
        result[n] = an
    return result


def find_antinodes_b(size, nodes):
    "expended beyond that"
    on_map = lambda p: 0 <= p[0] < size[0] and 0 <= p[1] < size[1]

    result = {}
    for n, nlist in nodes.items():
        ln = len(nlist)
        an = set()
        # foreach node pair
        for i in range(ln - 1):
            for j in range(i + 1, ln):
                na, nb = nlist[i], nlist[j]
                dx, dy = nb[0] - na[0], nb[1] - na[1]
                # extending past B
                while on_map(nb):
                    an.add(nb)
                    nb = (nb[0] + dx, nb[1] + dy)
                # extending before A
                while on_map(na):
                    an.add(na)
                    na = (na[0] - dx, na[1] - dy)
        result[n] = an
    return result


def day08a(fname):
    size, nodes = parse_data(fname)
    anti = find_antinodes(size, nodes)
    # need to remove the overlapping antinodes
    allanti = set()
    for _, an in anti.items():
        allanti.update(an)
    return len(allanti)


def day08b(fname):
    size, nodes = parse_data(fname)
    anti = find_antinodes_b(size, nodes)
    ##    print(anti)
    # need to remove the overlapping antinodes
    allanti = set()
    for _, an in anti.items():
        allanti.update(an)
    return len(allanti)


################################################################
if __name__ == "__main__":
    print("day08a", day08a("input08.txt"))
    print("day08b", day08b("input08.txt"))

################################################################


def test_parse_data():
    size, nodes = parse_data("test08.txt")
    assert size == (12, 12)
    assert len(nodes) == 2
    assert len(nodes["A"]) == 3
    assert len(nodes["0"]) == 4
    assert (5, 2) in nodes["0"]
    assert (6, 5) in nodes["A"]


def test_find_antinodes1():
    """test case 1:
        ..........
        ...#......
        ..........
        ....a.....
        ..........
        .....a....
        ..........
        ......#...
        ..........
        ..........
    10x10 grid, 2 nodes, 2 anti found"""
    size = (10, 10)
    nodes = {"a": [(4, 3), (5, 5)]}
    result = find_antinodes(size, nodes)
    print(result)
    assert len(result["a"]) == 2
    assert (3, 1) in result["a"]
    assert (6, 7) in result["a"]


def test_find_antinodes2():
    """test case 2:
        ..........
        ...#......
        #.........
        ....a.....
        ........a.
        .....a....
        ..#.......
        ......#...
        ..........
        ..........
    10x10 grid, 3 nodes, 4 anti found (2 off map)"""
    size = (10, 10)
    nodes = {"a": [(4, 3), (5, 5), (8, 4)]}
    result = find_antinodes(size, nodes)
    print(result)
    assert len(result["a"]) == 4
    assert (3, 1) in result["a"]
    assert (6, 7) in result["a"]
    assert (0, 2) in result["a"]
    assert (2, 6) in result["a"]


def test_find_antinodes3():
    """test case 3:
        ..........
        ...#......
        #.........
        ....a.....
        ........a.
        .....a....
        ..#.......
        ......A...
        ..........
        ..........
    10x10 grid, 3 nodes, 4 anti found (2 off map), one is on the A"""
    size = (10, 10)
    nodes = {"a": [(4, 3), (5, 5), (8, 4)], "A": [(6, 7)]}
    result = find_antinodes(size, nodes)
    print(result)
    assert len(result["a"]) == 4
    assert (3, 1) in result["a"]
    assert (6, 7) in result["a"]
    assert (0, 2) in result["a"]
    assert (2, 6) in result["a"]


def test_day08a():
    assert day08a("test08.txt") == 14


def test_find_antinodes_b():
    """test case:
        T....#....
        ...T......
        .T....#...
        .........#
        ..#.......
        ..........
        ...#......
        ..........
        ....#.....
        ..........
    10x10 grid, 3 nodes, 6 anti found"""
    size = (10, 10)
    nodes = {"T": [(0, 0), (3, 1), (1, 2)]}
    result = find_antinodes_b(size, nodes)
    print(result)
    assert len(result["T"]) == 9
    assert (5, 0) in result["T"]
    assert (6, 2) in result["T"]
    assert (9, 3) in result["T"]
    assert (2, 4) in result["T"]
    assert (3, 6) in result["T"]
    assert (4, 8) in result["T"]
    # the nodes are also aninodes
    assert (0, 0) in result["T"]
    assert (3, 1) in result["T"]
    assert (1, 2) in result["T"]


def test_day08b():
    assert day08b("test08.txt") == 34
