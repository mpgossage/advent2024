import pytest
import math
from helpers import load_tokens

""" Reading this I have a good idea where this is going.
Part A is the path planner.
Part B is a little simpler than expected, but its going to be a fun challenge
"""

DIR = [(1, 0), (0, 1), (-1, 0), (0, -1)]
WALL, SPACE = "#", "."
BIG = 1e7


def parse_data(fname):
    "returns [(x,y)]"
    result = []
    for tokens in load_tokens(fname, ","):
        result.append(tuple(int(v) for v in tokens))
    return result


def coords_to_grid(coords):
    "returns a 2d grid of WALL & SPACE"
    ## assumption area is square & the max value can be from the data
    size = 0
    for x, y in coords:
        size = max(size, x, y)
    size += 1
    # build grid
    grid = []
    for y in range(size):
        grid.append([SPACE] * size)
    #
    for x, y in coords:
        grid[y][x] = WALL
    return grid


def path_plan(coords, sx, sy):
    goal = sx - 1, sy - 1

    walls = set(coords)
    p = (0, 0)
    todo = {p: 0}
    visited = {p: 0}
    while todo:
        # find lowest cost
        pos, cost = None, BIG
        for k, v in todo.items():
            if cost > v:
                pos, cost = k, v
        del todo[pos]
        px, py = pos
        for dx, dy in DIR:
            n = (px + dx, py + dy)
            ncost = cost + 1
            if 0 <= n[0] < sx and 0 <= n[1] < sy and n not in walls:
                if visited.get(n, BIG) > ncost:
                    visited[n] = ncost
                    todo[n] = ncost
                    # end condition
                    if n == goal:
                        return ncost
    return None


def day18a(fname, num, size):
    coords = parse_data(fname)
    return path_plan(coords[:num], size, size)


def day18b(fname, start, size):
    coords = parse_data(fname)
    print("num coords", len(coords))
    # brute force for now
    for num in range(start, len(coords)):
        if path_plan(coords[:num], size, size) == None:
            return coords[num - 1]


################################################################
if __name__ == "__main__":
    print("day18a", day18a("input18.txt", 1024, 71))
    print("day18b", day18b("input18.txt", 1024, 71))


################################################################


def test_parse_data():
    data = parse_data("test18.txt")
    assert len(data) == 25
    assert data[0] == (5, 4)
    assert data[-1] == (2, 0)


def test_coords_to_grid():
    data = parse_data("test18.txt")
    data = data[:12]  # first 12 for testing
    grid = coords_to_grid(data)
    assert len(grid) == 7
    assert len(grid[0]) == 7
    assert "".join(grid[0]) == "...#..."
    assert "".join(grid[-1]) == "#.#...."


def test_path_plan():
    data = parse_data("test18.txt")
    data = data[:12]  # first 12 for testing
    assert path_plan(data, 7, 7) == 22


def test_day18a():
    assert day18a("test18.txt", 12, 7) == 22


def test_day18b():
    assert day18b("test18.txt", 12, 7) == (6, 1)
