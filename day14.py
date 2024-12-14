import pytest
import math
import re
import os
from helpers import load_lines
from PIL import Image

# part A easy
# Part B is a WTF!
# going to make a guess and say its symetrical, so looking for a symetical pattern
# failed: using pillow to make a lot of images!
# The image is not in the middle of the screen, locating it needed to be done by eye


def parse_data(fname):
    "returns [((px,py),(vx,vy))...]"
    pattern = re.compile(r"p=(.*),(.*) v=(.*),(.*)")
    result = []
    for line in load_lines(fname):
        m = pattern.search(line)
        if m:
            p = (int(m.group(1)), int(m.group(2)))
            v = (int(m.group(3)), int(m.group(4)))
            result.append((p, v))
    return result


def move_robots(robots, steps, sx, sy):
    "moves the robots accordingly & returns [(x,y)..]"
    result = []
    for p, v in robots:
        x, y = p[0] + v[0] * steps, p[1] + v[1] * steps
        # wrap (python wrap handles -ve correctly an ends up 0..N-1)
        x %= sx
        y %= sy
        result.append((x, y))
    return result


def day14a(fname, sx, sy):
    "note: needs size as it changes based upon the data"
    robots = parse_data(fname)
    final_pos = move_robots(robots, 100, sx, sy)
    # quadrent them
    quads = [[0, 0], [0, 0]]  # a 2d array
    sx2, sy2 = sx // 2, sy // 2
    for px, py in final_pos:
        if px == sx2 or py == sy2:
            continue  # ignore the middle ones
        ix, iy = 0, 0
        if px > sx2:
            ix = 1
        if py > sx2:
            iy = 1
        quads[iy][ix] += 1
    return quads[0][0] * quads[0][1] * quads[1][0] * quads[1][1]


def display(positions, sx, sy):
    "hack to print positions"
    for y in range(sy):
        line = ["."] * sx
        for px, py in positions:
            if py == y:
                line[px] = "*"
        print("".join(line))


def day14b_slow(fname, sx, sy):
    "looks for symetrical & prints, too slow with 1 millon"
    robots = parse_data(fname)
    for t in range(1000 * 1000):
        final_pos = move_robots(robots, t, sx, sy)
        symetrical = True
        for px, py in final_pos:
            if (sx - 1 - px, py) not in final_pos:
                symetrical = False
                break

        # if symetical try
        if symetrical:
            # print!!!
            print("time", t)
            display(final_pos, sx, sy)
        if t % 1000 == 0:
            print(t)


def day14b(fname, sx, sy):
    "attempting to speed it"
    robots = parse_data(fname)

    pos = [list(p) for p, v in robots]
    vel = [list(p) for p, v in robots]
    numr = len(robots)
    for t in range(1000 * 1000 * 1000):
        for i in range(numr):
            pos[i][0] = (pos[i][0] + vel[i][0]) % sx
            pos[i][1] = (pos[i][1] + vel[i][1]) % sy
        symetrical = True
        for px, py in pos:
            if (sx - 1 - px, py) not in pos:
                symetrical = False
                break

        # if symetical try
        if symetrical:
            # print!!!
            print("time", t)
            display(pos, sx, sy)
            return
        if t % 10000 == 0:
            print(t)


def day14b_image(fname, sx, sy, num):
    "making a Sh!t ton of images"
    robots = parse_data(fname)

    os.makedirs("day14b", 0o777, True)
    for t in range(num):
        final_pos = move_robots(robots, t, sx, sy)
        img = Image.new(mode="RGB", size=(sx, sy))
        for p in final_pos:
            img.putpixel(p, (255, 255, 255))
        img.save(f"day14b/img{t:05}.jpg")


################################################################
if __name__ == "__main__":
    print("day14a", day14a("input14.txt", 101, 103))
    # day14b("input14.txt",101,103)
    day14b_image("input14.txt", 101, 103, 10000)


################################################################


def test_parse_data():
    data = parse_data("test14.txt")
    assert len(data) == 12
    assert data[0] == ((0, 4), (3, -3))
    assert data[-1] == ((9, 5), (-3, -3))


def test_move_robots():
    robot = ((2, 4), (2, -3))
    assert move_robots([robot], 0, 11, 7) == [(2, 4)]
    assert move_robots([robot], 1, 11, 7) == [(4, 1)]
    assert move_robots([robot], 2, 11, 7) == [(6, 5)]
    assert move_robots([robot], 3, 11, 7) == [(8, 2)]
    assert move_robots([robot], 4, 11, 7) == [(10, 6)]
    assert move_robots([robot], 5, 11, 7) == [(1, 3)]


def test_day14a():
    assert day14a("test14.txt", 11, 7) == 12
