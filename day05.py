import pytest
import re
from helpers import load_lines


def parse_data(fname):
    """returns ordering & updates in the form [(a,b)...],[[a,b,c]...]"""
    ordering, updates = [], []
    is_order = True
    for l in load_lines(fname):
        if l == "":
            is_order = False
        elif is_order:
            arr = [int(v) for v in l.split("|")]
            ordering.append((arr[0], arr[1]))
        else:
            updates.append([int(v) for v in l.split(",")])

    return ordering, updates


def is_valid_update(ordering, update):
    "returns if the update obeys the ordering"
    for oa, ob in ordering:
        if oa in update and ob in update:
            if update.index(oa) > update.index(ob):
                return False
    return True


def day05a(fname):
    ordering, updates = parse_data(fname)
    total = 0
    for up in updates:
        if is_valid_update(ordering, up):
            midval = up[len(up) // 2]
            total += midval
    return total


def reorder_update(ordering, update):
    "returns the reordered update"
    # when in doubt, simplest thing that works:
    # if an ordering fails, swap the two elements and try again
    while True:
        ordered = True
        for oa, ob in ordering:
            if oa in update and ob in update:
                ia, ib = update.index(oa), update.index(ob)
                if ia > ib:
                    update[ib] = oa
                    update[ia] = ob
                    ordered = False
        if ordered:
            return update


def day05b(fname):
    ordering, updates = parse_data(fname)
    total = 0
    for up in updates:
        if is_valid_update(ordering, up) == False:
            up = reorder_update(ordering, up)
            midval = up[len(up) // 2]
            total += midval
    return total


################################################################
if __name__ == "__main__":
    print("day05a", day05a("input05.txt"))
    print("day05b", day05b("input05.txt"))

################################################################


def test_parse_data():
    ordering, updates = parse_data("test05.txt")
    assert len(ordering) == 21
    assert ordering[0] == (47, 53)
    assert ordering[-1] == (53, 13)
    assert len(updates) == 6
    assert updates[0] == [75, 47, 61, 53, 29]
    assert updates[-1] == [97, 13, 75, 29, 47]


def test_is_valid_update():
    ordering, updates = parse_data("test05.txt")
    assert is_valid_update(ordering, updates[0])
    assert is_valid_update(ordering, updates[1])
    assert is_valid_update(ordering, updates[2])
    assert is_valid_update(ordering, updates[3]) == False
    assert is_valid_update(ordering, updates[4]) == False
    assert is_valid_update(ordering, updates[5]) == False


def test_day05a():
    assert day05a("test05.txt") == 143


def test_reorder_update():
    ordering, updates = parse_data("test05.txt")

    # correct is unchanged
    assert reorder_update(ordering, updates[0]) == updates[0]
    assert reorder_update(ordering, updates[1]) == updates[1]
    assert reorder_update(ordering, updates[2]) == updates[2]
    # others are fixed
    assert reorder_update(ordering, updates[3]) == [97, 75, 47, 61, 53]
    assert reorder_update(ordering, updates[4]) == [61, 29, 13]
    assert reorder_update(ordering, updates[5]) == [97, 75, 47, 29, 13]


def test_day05b():
    assert day05b("test05.txt") == 123
