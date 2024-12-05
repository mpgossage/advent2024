import pytest
import re
from helpers import load_lines


def grid_find(text, grid, x, y, dx, dy):
    """returns true if text is held in grid starting at x,y and moving dx,dy"""
    w, h = len(grid[0]), len(grid)
    for t in text:
        if not (0 <= x < w and 0 <= y < h and grid[y][x] == t):
            return False
        x += dx
        y += dy
    return True


def day04a(fname):
    grid = load_lines(fname)
    w, h = len(grid[0]), len(grid)
    text = "XMAS"
    directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

    total = 0
    for y in range(h):
        for x in range(w):
            for d in directions:
                if grid_find(text, grid, x, y, d[0], d[1]):
                    total += 1
    return total


def day04b(fname):
    grid = load_lines(fname)
    w, h = len(grid[0]), len(grid)
    text = "MAS"
    directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]

    # logic: to find a X-MAS starting at x,y we need
    # find the MAS on the \ diagonal
    # which is grid_find(...x,y,1,1) or grid_find(...x+2,y+2,-1,-1)
    # find the MAS on the / diagonal
    # which is grid_find(...x+2,y,-1,1) or grid_find(...x,y+2,1,-1)
    total = 0
    for y in range(h):
        for x in range(w):
            if grid_find(text, grid, x, y, 1, 1) or grid_find(
                text, grid, x + 2, y + 2, -1, -1
            ):
                if grid_find(text, grid, x + 2, y, -1, 1) or grid_find(
                    text, grid, x, y + 2, 1, -1
                ):
                    total += 1
    return total


################################################################
if __name__ == "__main__":
    print("day04a", day04a("input04.txt"))
    print("day04b", day04b("input04.txt"))

################################################################


def test_day04a():
    assert day04a("test04.txt") == 18


def test_day04b():
    assert day04b("test04.txt") == 9
