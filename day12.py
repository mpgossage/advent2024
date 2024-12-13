import pytest
import math
from helpers import load_lines

# part A easy, part B a real head scratching


DIR = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def explore_region(grid, pos):
    "given a grid & pos returns the whole region in the form set(pos)"
    # standard looking BFS
    sx, sy = len(grid[0]), len(grid)
    region = set()
    todo = set()
    todo.add(pos)
    val = grid[pos[1]][pos[0]]
    while len(todo) > 0:
        p = todo.pop()
        if p in region:
            continue
        region.add(p)
        px, py = p
        for dx, dy in DIR:
            nx, ny = px + dx, py + dy
            if 0 <= nx < sx and 0 <= ny < sy and grid[ny][nx] == val:
                todo.add((nx, ny))
    return region


def calc_perimeter(region):
    "simple really: for each cell, count adjacent cells not in region"
    perim = 0
    for rx, ry in region:
        for dx, dy in DIR:
            nx, ny = rx + dx, ry + dy
            if (nx, ny) not in region:
                perim += 1
    return perim


def calc_edges(region):
    """how?
    Here is an idea:
    A top edge is (x1,y,x2) which means x1,y...x2,y are all in region but north is not
    We find a point & search left/right to find the limits, then add it.
    Similar for all other directions.
    Feels hard, but rather than then try to merge all edging bits
    """
    topedges = set()
    for rx, ry in region:
        if (rx, ry - 1) not in region:
            # look both directions
            x1, x2, y = rx, rx, ry
            while (x1 - 1, y) in region and (x1 - 1, y - 1) not in region:
                x1 -= 1
            while (x2 + 1, y) in region and (x2 + 1, y - 1) not in region:
                x2 += 1
            # note: we could look for dups, but the set will remove the dups
            topedges.add((x1, y, x2))
    bottomedges = set()
    for rx, ry in region:
        if (rx, ry + 1) not in region:
            x1, x2, y = rx, rx, ry
            while (x1 - 1, y) in region and (x1 - 1, y + 1) not in region:
                x1 -= 1
            while (x2 + 1, y) in region and (x2 + 1, y + 1) not in region:
                x2 += 1
            bottomedges.add((x1, y, x2))
    leftedges = set()
    for rx, ry in region:
        if (rx - 1, ry) not in region:
            x, y1, y2 = rx, ry, ry
            while (x, y1 - 1) in region and (x - 1, y1 - 1) not in region:
                y1 -= 1
            while (x, y2 + 1) in region and (x - 1, y2 + 1) not in region:
                y2 += 1
            leftedges.add((x, y1, y2))
    rightedges = set()
    for rx, ry in region:
        if (rx + 1, ry) not in region:
            x, y1, y2 = rx, ry, ry
            while (x, y1 - 1) in region and (x + 1, y1 - 1) not in region:
                y1 -= 1
            while (x, y2 + 1) in region and (x + 1, y2 + 1) not in region:
                y2 += 1
            rightedges.add((x, y1, y2))
    ##    print("top",topedges,"bottom",bottomedges)
    ##    print("left",leftedges,"right",rightedges)
    return len(topedges) + len(bottomedges) + len(leftedges) + len(rightedges)


def day12a(fname):
    grid = load_lines(fname)
    sx, sy = len(grid[0]), len(grid)
    explored = set()
    total = 0
    for y in range(sy):
        for x in range(sx):
            if (x, y) not in explored:
                region = explore_region(grid, (x, y))
                perim = calc_perimeter(region)
                size = len(region)
                total += size * perim
                explored.update(region)
    return total


def day12b(fname):
    grid = load_lines(fname)
    sx, sy = len(grid[0]), len(grid)
    explored = set()
    total = 0
    for y in range(sy):
        for x in range(sx):
            if (x, y) not in explored:
                region = explore_region(grid, (x, y))
                edges = calc_edges(region)
                size = len(region)
                total += size * edges
                explored.update(region)
    return total


################################################################
if __name__ == "__main__":
    print("day12a", day12a("input12.txt"))
    print("day12b", day12b("input12.txt"))

################################################################


def test_explore_region1():
    grid = load_lines("test12a.txt")
    region = explore_region(grid, (0, 0))
    assert region == set([(0, 0), (1, 0), (2, 0), (3, 0)])

    region = explore_region(grid, (0, 1))
    assert region == set([(0, 1), (1, 1), (0, 2), (1, 2)])

    region = explore_region(grid, (2, 1))
    assert region == set([(2, 1), (2, 2), (3, 2), (3, 3)])

    region = explore_region(grid, (3, 1))
    assert region == set([(3, 1)])

    region = explore_region(grid, (0, 3))
    assert region == set([(0, 3), (1, 3), (2, 3)])


def test_explore_region2():
    grid = load_lines("test12b.txt")
    # not checking all, just that the X's are seperate
    region = explore_region(grid, (1, 1))
    assert region == set([(1, 1)])

    region = explore_region(grid, (3, 3))
    assert region == set([(3, 3)])

    assert len(explore_region(grid, (0, 0))) == 21


def test_calc_perimeter1():
    grid = load_lines("test12a.txt")
    region = explore_region(grid, (0, 0))
    assert calc_perimeter(region) == 10

    assert calc_perimeter(explore_region(grid, (0, 1))) == 8

    assert calc_perimeter(explore_region(grid, (3, 1))) == 4


def test_calc_perimeter2():
    grid = load_lines("test12b.txt")
    region = explore_region(grid, (0, 0))
    assert calc_perimeter(region) == 36


def test_day12a():
    assert day12a("test12a.txt") == 140
    assert day12a("test12b.txt") == 772
    assert day12a("test12c.txt") == 1930


def test_calc_edges1():
    grid = load_lines("test12a.txt")
    region = explore_region(grid, (0, 0))
    assert calc_edges(region) == 4

    assert calc_edges(explore_region(grid, (0, 1))) == 4

    assert calc_edges(explore_region(grid, (2, 1))) == 8


def test_day12b():
    assert day12b("test12a.txt") == 80
    assert day12b("test12b.txt") == 436
    assert day12b("test12c.txt") == 1206
    assert day12b("test12d.txt") == 236
    assert day12b("test12e.txt") == 368
