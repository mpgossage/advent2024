import pytest
import re
from helpers import load_lines

"""PartB failed using a simple, add one cell and run 20K steps to see if it ends.
Reason is that there are too many steps total.
Instead looking at turns & counting them.
Still turned out to be too slow as 130x130 has ~17K locations.
Was able to reduce to ~5K locations by only using the steps the guard visited.
Saved a chunk more by using sets instead of lists
"""

DIR = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # NESW


def parse_data(fname):
    "returns guard pos, obstacles & size in the form (gx,gy),[(o1x,o1y),(o2x,o2y),...]"
    guard, obstacles = None, []
    grid = load_lines(fname)
    for y, line in enumerate(grid):
        for x, v in enumerate(line):
            if v == "^":
                guard = (x, y)
            elif v == "#":
                obstacles.append((x, y))
    return guard, obstacles, (len(grid[0]), len(grid))


def day06a(fname):
    guard, obstacles, size = parse_data(fname)
    direct = 0
    x, y = guard
    steps = set()
    while 0 <= x < size[0] and 0 <= y < size[1]:
        steps.add((x, y))
        nx, ny = x + DIR[direct][0], y + DIR[direct][1]
        if (nx, ny) in obstacles:
            direct = (direct + 1) % len(DIR)
        else:
            x, y = nx, ny
    return len(steps)


def is_infinite_loop(guard, obstacles, size):
    # check for infinite loop
    # XXX using 20K steps at forever as partA was only 4.5K XXX
    # fails with real data, switching to tracking the turns & looking for a repeat

    # micro optimisation: its MUCH quicker to lookup a set then a list
    # so store the obstacles in a set
    obstacles = set(obstacles)
    direct = 0
    x, y = guard
    turns = set()
    while 0 <= x < size[0] and 0 <= y < size[1]:
        nx, ny = x + DIR[direct][0], y + DIR[direct][1]
        if (nx, ny) in obstacles:
            if (x, y, direct) in turns:
                return True
            turns.add((x, y, direct))
            direct = (direct + 1) % len(DIR)
        else:
            x, y = nx, ny
    return False


def day06b(fname):
    # again simplest thing that works
    # XXX foreach possible pos, add an obstacle & see if it takes forever XXX
    # fails: instead track places the guard goes, it has to be one of those

    guard, obstacles, size = parse_data(fname)

    # step 1: get a list of all places explored:
    # duplicating the navigate code
    direct = 0
    x, y = guard
    steps = set()
    while 0 <= x < size[0] and 0 <= y < size[1]:
        steps.add((x, y))
        nx, ny = x + DIR[direct][0], y + DIR[direct][1]
        if (nx, ny) in obstacles:
            direct = (direct + 1) % len(DIR)
        else:
            x, y = nx, ny

    # step 2: for each step put an obstacle there & try
    count = 0
    for x, y in steps:
        if (x, y) == guard or (x, y) in obstacles:
            continue
        if is_infinite_loop(guard, obstacles + [(x, y)], size):
            count += 1
    return count


################################################################
if __name__ == "__main__":
    print("day06a", day06a("input06.txt"))
    print("day06b", day06b("input06.txt"))

################################################################


def test_parse_data():
    guard, obstacles, size = parse_data("test06.txt")
    assert guard == (4, 6)
    assert size == (10, 10)
    assert len(obstacles) == 8
    assert (4, 0) in obstacles
    assert (6, 9) in obstacles


def test_day06a():
    assert day06a("test06.txt") == 41


def test_is_infinite_loop():
    guard, obstacles, size = parse_data("test06.txt")
    assert is_infinite_loop(guard, obstacles, size) == False
    assert is_infinite_loop(guard, obstacles + [(0, 0)], size) == False
    assert is_infinite_loop(guard, obstacles + [(3, 6)], size) == True
    assert is_infinite_loop(guard, obstacles + [(7, 9)], size) == True


def test_day06b():
    assert day06b("test06.txt") == 6
