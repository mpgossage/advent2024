import pytest
import math
import sys
from helpers import load_lines

""" Part A, fairly simple.
Part B, my default BFS algo only handles finding a single path,
this needs to find all the best paths.
This was a lot more complex than I expected
"""

DIR = [(1, 0), (0, 1), (-1, 0), (0, -1)]
WALL = "#"
COSTM = 1
COSTT = 1000
BIG = 1e7


def find_cell(grid, val):
    for y, line in enumerate(grid):
        for x, v in enumerate(line):
            if v == val:
                return x, y


def day16a(fname):
    # helper:
    get_cost = lambda data, pos: data.get(pos, BIG)

    # setup
    grid = load_lines(fname)
    start = find_cell(grid, "S")
    end = find_cell(grid, "E")
    p = (start[0], start[1], 0)
    todo = {p: 0}
    visited = {}
    count = 0
    while todo:
        # lowest cost
        pos, cost = None, BIG
        for k, v in todo.items():
            if v < cost:
                pos, cost = k, v
        del todo[pos]
        ##        print("process",pos,cost)
        # end condition:
        if pos[0] == end[0] and pos[1] == end[1]:
            return cost

        # if visited & cost is better, skip
        if get_cost(visited, pos) <= cost:
            continue
        visited[pos] = cost

        px, py, pa = pos
        # add turn
        left = (px, py, (pa + 3) % 4)
        right = (px, py, (pa + 1) % 4)
        if get_cost(todo, left) > cost + COSTT:
            todo[left] = cost + COSTT
        if get_cost(todo, right) > cost + COSTT:
            todo[right] = cost + COSTT

        # if you can move fowards:
        nx, ny = px + DIR[pa][0], py + DIR[pa][1]
        forward = (nx, ny, pa)
        if grid[ny][nx] != WALL and get_cost(todo, forward) > cost + COSTM:
            todo[forward] = cost + COSTM

        count += 1
        if count % 1000 == 0:
            print("best", cost, "todo", len(todo), "visited", len(visited))
            sys.stdout.flush()
    print("ran out of todo")


def day16b(fname):
    # helper:
    get_cost = lambda data, pos: data.get(pos, (BIG, None))[0]

    def add_done(data, pos, cost, prev):
        if get_cost(data, pos) < cost:
            return  # ignore big costs
        if pos not in data or data[pos][0] > cost:
            data[pos] = (cost, set([prev]))
        else:
            data[pos][1].add(prev)

    # setup
    grid = load_lines(fname)
    start = find_cell(grid, "S")
    end = find_cell(grid, "E")
    p = (start[0], start[1], 0)
    todo = {p: (0, None)}  # pos=>(cost,prev)
    visited = {p: (0, set())}  # pos=>(cost,set(prev))
    route_cost = None  # None/cost
    count = 0
    while todo:
        # lowest cost
        pos, cost, prev = None, BIG, None
        for k, v in todo.items():
            if v[0] < cost:
                pos, cost, prev = k, v[0], v[1]
        del todo[pos]

        # if finished: ignore those with too high cost
        if route_cost and cost > route_cost:
            continue

        # if visited & cost is better, skip
        if get_cost(visited, pos) < cost:
            continue

        px, py, pa = pos
        # add turn
        left = (px, py, (pa + 3) % 4)
        right = (px, py, (pa + 1) % 4)
        if get_cost(visited, left) >= cost + COSTT:
            todo[left] = (cost + COSTT, pos)
            add_done(visited, left, cost + COSTT, pos)
        if get_cost(visited, right) >= cost + COSTT:
            todo[right] = (cost + COSTT, pos)
            add_done(visited, right, cost + COSTT, pos)

        # if you can move fowards:
        nx, ny = px + DIR[pa][0], py + DIR[pa][1]
        forward = (nx, ny, pa)
        if grid[ny][nx] != WALL and get_cost(visited, forward) >= cost + COSTM:
            todo[forward] = (cost + COSTM, pos)
            add_done(visited, forward, cost + COSTM, pos)
            # end condition:
            if (nx,ny) == end:
                print("found route for cost", cost + COSTM)
                route_cost = cost + COSTM
                continue

        count += 1
        if count % 1000 == 0:
            print("best", cost, "todo", len(todo), "visited", len(visited))
            sys.stdout.flush()

    # so we have a list of all visited nodes & the previous nodes
    # go through all previous nodes & get the viewing places

    # todo can be any direction
    todo = set()
    for a in range(4):
        todo.add((end[0], end[1], a))
    view = set()  # (x,y)

    while todo:
        pos = todo.pop()
        view.add((pos[0], pos[1]))
        _, prevs = visited.get(pos, (0, []))
        for pr in prevs:
            todo.add(pr)
    return len(view)


################################################################
if __name__ == "__main__":
    print("day16a", day16a("input16.txt"))
    print("day16b", day16b("input16.txt"))

################################################################


def test_find_cell():
    grid = load_lines("test16a.txt")
    assert (1, 13) == find_cell(grid, "S")
    assert (13, 1) == find_cell(grid, "E")


def test_day16a():
    assert day16a("test16a.txt") == 7036
    assert day16a("test16b.txt") == 11048


def test_day16b():
    assert day16b("test16a.txt") == 45
    assert day16b("test16b.txt") == 64
