import pytest
import math
from helpers import load_lines

# not having a parse, for this fn, just going to use the list of strings
# reasonable sure that part B is almost a simplification

DIR = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def count_trailhead(grid, pos):
    """returns the number of reachable trailheads from the given start pos.
    simplest thing that works, use a BFS and find all the reachable 9's.
    Part B may change the rules completely, but keeping it simple rather
    than trying to guess the part B."""
    sx, sy = len(grid[0]), len(grid)
    trailhead = 0
    visited = set()
    todo = set()  # arbitary set, no priority ordering here
    todo.add(pos)
    ##    print("start: visited",visited,"todo",todo)
    while len(todo) > 0:
        p = todo.pop()
        ##        print("pos",p,"visited",visited,"todo",todo)
        px, py = p[0], p[1]
        val = grid[py][px]
        if val == "9":
            # if end of line, add the visited & skip
            if p not in visited:
                trailhead += 1
            visited.add(p)
            continue

        visited.add(p)
        newval = str(int(val) + 1)
        # look in all directions for the next step up
        for d in DIR:
            nx, ny = px + d[0], py + d[1]
            if (
                0 <= nx < sx
                and 0 <= ny < sy
                and grid[ny][nx] == newval
                and (nx, ny) not in visited
            ):
                todo.add((nx, ny))

    return trailhead


def day10a(fname):
    result = 0
    grid = load_lines(fname)
    for y, line in enumerate(grid):
        for x, val in enumerate(line):
            if val == "0":
                result += count_trailhead(grid, (x, y))
    return result


def count_trailrating(grid, pos):
    """This is generally a simplification, as we BFS but we permit mutiple routes
    to a single location. So we don't need to track visited & not use a set"""
    sx, sy = len(grid[0]), len(grid)
    rating = 0
    todo = [pos]
    ##    print("start: todo",todo)
    while len(todo) > 0:
        p = todo.pop(-1)
        px, py = p[0], p[1]
        val = grid[py][px]
        ##        print("pos",p,"val",val,"todo",todo)
        if val == "9":
            # if end of line, its a route so it adds rating
            rating += 1
            continue

        newval = str(int(val) + 1)
        # look in all directions for the next step up
        for d in DIR:
            nx, ny = px + d[0], py + d[1]
            if 0 <= nx < sx and 0 <= ny < sy and grid[ny][nx] == newval:
                todo.append((nx, ny))

    return rating


def day10b(fname):
    result = 0
    grid = load_lines(fname)
    for y, line in enumerate(grid):
        for x, val in enumerate(line):
            if val == "0":
                result += count_trailrating(grid, (x, y))
    return result


################################################################
if __name__ == "__main__":
    print("day10a", day10a("input10.txt"))
    print("day10b", day10b("input10.txt"))

################################################################


def test_count_trailhead1():
    data = """0123
1234
8765
9876""".split(
        "\n"
    )
    assert count_trailhead(data, (0, 0)) == 1


def test_count_trailhead2():
    data = """...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9""".split(
        "\n"
    )
    assert count_trailhead(data, (3, 0)) == 2


def test_count_trailhead3():
    data = """..90..9
...1.98
...2..7
6543456
765.987
876....
987....""".split(
        "\n"
    )
    assert count_trailhead(data, (3, 0)) == 4


def test_count_trailhead4():
    data = """10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01""".split(
        "\n"
    )
    assert count_trailhead(data, (1, 0)) == 1
    assert count_trailhead(data, (5, 6)) == 2


def test_count_trailhead5():
    data = load_lines("test10.txt")
    assert count_trailhead(data, (2, 0)) == 5
    assert count_trailhead(data, (4, 0)) == 6
    assert count_trailhead(data, (4, 2)) == 5
    assert count_trailhead(data, (6, 4)) == 3
    assert count_trailhead(data, (2, 5)) == 1
    assert count_trailhead(data, (5, 5)) == 3
    assert count_trailhead(data, (0, 6)) == 5
    assert count_trailhead(data, (6, 6)) == 3
    assert count_trailhead(data, (1, 7)) == 5


def test_day10a():
    assert day10a("test10.txt") == 36


def test_count_trailrating1():
    data = """.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....""".split(
        "\n"
    )
    assert count_trailrating(data, (5, 0)) == 3


def test_count_trailrating2():
    data = """..90..9
...1.98
...2..7
6543456
765.987
876....
987....""".split(
        "\n"
    )
    assert count_trailrating(data, (3, 0)) == 13


def test_count_trailrating3():
    data = """012345
123456
234567
345678
4.6789
56789.""".split(
        "\n"
    )
    assert count_trailrating(data, (0, 0)) == 227


def test_day10b():
    assert day10b("test10.txt") == 81
