"""
Advent of Code 2024: helpers
"""


def load_file(fname):
    with open(fname) as f:
        return f.read()


def load_lines(fname):
    with open(fname) as f:
        return [l.strip("\n") for l in f.readlines()]


def load_tokens(fname, sep=None):
    with open(fname) as f:
        return [l.strip("\n").split(sep) for l in f.readlines()]


def load_int_tokens(fname, sep=None):
    """loads a file and parses it as a 2d array of space seperated integers"""
    with open(fname) as f:
        result = []
        for l in f:
            result.append([int(v) for v in l.strip("\n").split(sep)])
        return result


def load_int_grid(fname):
    """loads a 2d grid of numbers and returns a Y-X grid.
    so grid[y][x] is the item you want"""
    grid = []
    with open(fname) as f:
        for l in f.readlines():
            grid.append([int(a) for a in l.strip("\n")])
    return grid
