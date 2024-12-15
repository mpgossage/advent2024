import pytest
import math
from helpers import load_lines

# Part A: fairly simple
# Part B: "the horror", took a good chunk of thinking

MOVE = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}
ROB = "@"
BOX = "O"
WALL = "#"
SPACE = "."

BOXL, BOXR = "[", "]"


def parse_data(fname):
    """returns [grid],"moves" """
    grid = []
    moves = []
    in_grid = True

    for line in load_lines(fname):
        if line == "":
            in_grid = False
        else:
            if in_grid:
                grid.append(line)
            else:
                moves.append(line)

    return grid, "".join(moves)


def print_grid(grid):
    for g in grid:
        print("".join(g))


def move_robot(grid, moves):
    "moves the robot & returns the modified grid"
    g = [list(l) for l in grid]
    rx, ry = 0, 0
    for y, line in enumerate(g):
        for x, v in enumerate(line):
            if v == ROB:
                rx, ry = x, y
                break
    ##    print("start")
    ##    print_grid(g)
    for m in moves:
        ##        print("move:",m)
        dx, dy = MOVE[m]
        nx, ny = rx + dx, ry + dy
        # can the robot move there?
        if g[ny][nx] == SPACE:
            g[ry][rx] = SPACE
            g[ny][nx] = ROB
            rx, ry = nx, ny
        elif g[ny][nx] == BOX:
            # its a box, can I push it?
            # look ahead and find an empty spot:
            # if its there I can push all to there, otherwise cannot move
            bx, by = nx, ny
            while g[by][bx] == BOX:
                bx, by = bx + dx, by + dy
            # space or wall?
            if g[by][bx] == WALL:
                # wall, don't move
                continue
            # its clear move all the boxes
            g[by][bx] = BOX
            g[ry][rx] = SPACE
            g[ny][nx] = ROB
            rx, ry = nx, ny
    ##        print_grid(g)

    return g


def calc_gps(grid):
    "returns the total GPS value"
    total = 0
    for y, line in enumerate(grid):
        for x, v in enumerate(line):
            if v == BOX or v == BOXL:
                total += (y * 100) + x
    return total


def day15a(fname):
    grid, moves = parse_data(fname)
    final = move_robot(grid, moves)
    return calc_gps(final)


def find_pushed_blocks(grid, bx, by, dx, dy):
    "returns list of blocks which will be pushed by box in bx,by (left) dx,dy (inc the block)"
    result = set()
    todo = set([(bx, by)])
    while todo:
        p = todo.pop()
        if p in result:
            continue
        result.add(p)
        x, y = p[0] + dx, p[1] + dy
        if grid[y][x] == BOXL:
            todo.add((x, y))
        elif grid[y][x] == BOXR:
            todo.add((x - 1, y))
        x += 1
        if grid[y][x] == BOXL:
            todo.add((x, y))
        elif grid[y][x] == BOXR:
            todo.add((x - 1, y))
    return list(result)


def can_push(grid, bx, by, dx, dy):
    "returns true if box in bx,by (left) can be moved dx,dy"
    blocks = find_pushed_blocks(grid, bx, by, dx, dy)
    ##    print("canpush",dx,dy,blocks)
    # check each block & see if it can be moved (not a wall)
    for b in blocks:
        x, y = b[0] + dx, b[1] + dy
        if grid[y][x] == WALL:
            return False
        if grid[y][x + 1] == WALL:
            return False
    return True


def do_push(grid, bx, by, dx, dy):
    "modifies grid to move box bx,by by dx,dy. confirmed is valid move"
    blocks = find_pushed_blocks(grid, bx, by, dx, dy)
    # remove all blocks, then put all blocks in the new space
    for b in blocks:
        x, y = b[0], b[1]
        grid[y][x] = SPACE
        grid[y][x + 1] = SPACE
    for b in blocks:
        x, y = b[0] + dx, b[1] + dy
        grid[y][x] = BOXL
        grid[y][x + 1] = BOXR


def move_robot2(grid, moves):
    "converts map to wide,moves the robot & returns the modified grid"
    g = []
    for line in grid:
        l = []
        for v in line:
            if v == WALL:
                l += [WALL, WALL]
            elif v == BOX:
                l += [BOXL, BOXR]
            elif v == SPACE:
                l += [SPACE, SPACE]
            elif v == ROB:
                l += [ROB, SPACE]
        g.append(l)
    rx, ry = 0, 0
    for y, line in enumerate(g):
        for x, v in enumerate(line):
            if v == ROB:
                rx, ry = x, y
                break
    ##    print("start")
    ##    print_grid(g)
    for m in moves:
        ##        print("move:",m)
        dx, dy = MOVE[m]
        nx, ny = rx + dx, ry + dy
        # can the robot move there?
        if g[ny][nx] == SPACE:
            ##            print("  moved")
            g[ry][rx] = SPACE
            g[ny][nx] = ROB
            rx, ry = nx, ny
        elif g[ny][nx] == BOXL or g[ny][nx] == BOXR:
            bx, by = nx, ny
            if g[by][bx] == BOXR:
                bx -= 1
            if can_push(g, bx, by, dx, dy):
                ##                print("  pushed")
                do_push(g, bx, by, dx, dy)
                # move rob
                g[ry][rx] = SPACE
                g[ny][nx] = ROB
                rx, ry = nx, ny
    ##            else:
    ##                print("  nopush")
    ##        print_grid(g)

    return g


def day15b(fname):
    grid, moves = parse_data(fname)
    final = move_robot2(grid, moves)
    for f in final:
        print("".join(f))
    return calc_gps(final)


################################################################
if __name__ == "__main__":
    print("day15a", day15a("input15.txt"))
    print("day15b", day15b("input15.txt"))


################################################################


def test_parse_data():
    grid, moves = parse_data("test15a.txt")
    assert len(grid) == 8
    assert len(grid[0]) == 8
    assert moves == "<^^>>>vv<v>>v<<"

    grid, moves = parse_data("test15b.txt")
    assert len(grid) == 10
    assert len(grid[0]) == 10
    assert len(moves) == 10 * 70


def test_move_robot():
    grid, moves = parse_data("test15a.txt")
    grid = move_robot(grid, moves)
    assert len(grid) == 8
    assert len(grid[0]) == 8
    assert grid[4][4] == "@"
    assert "".join(grid[1]) == "#....OO#"
    assert "".join(grid[4]) == "#.#O@..#"


def test_day15a():
    assert day15a("test15b.txt") == 10092


def test_move_robot2():
    grid, moves = parse_data("test15c.txt")
    grid = move_robot2(grid, moves)
    assert "".join(grid[1]) == "##...[].##..##"
    assert "".join(grid[2]) == "##...@.[]...##"
    assert "".join(grid[3]) == "##....[]....##"


def test_day15b():
    assert day15b("test15b.txt") == 9021
