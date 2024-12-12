import pytest
import math
from helpers import load_file

# part A ran a little slow, its a 94503 length array
# part B has a very different algorithm and needs a different data structure
# part B also ran slow


def parse_data(fname):
    "returns [int]"
    data = load_file(fname).strip("\n")
    return [int(d) for d in data]


def dense_to_sparse(dense):
    """converts dense '12345' to sparse '0..111....22222'
    but in a [str] format rather than a true string"""
    result = []
    num = 0
    idx, ln = 0, len(dense)
    while idx < ln:
        # add X numbers
        result += [num] * dense[idx]
        idx += 1
        num += 1
        if idx < ln:
            # add empties
            result += ["."] * dense[idx]
            idx += 1
    return result


def compress_sparse(sparse):
    "compresses the sparse array and returns it"
    while "." in sparse:
        idx = sparse.index(".")
        v = sparse.pop(-1)
        sparse[idx] = v
        while sparse[-1] == ".":
            sparse.pop(-1)
    return sparse


def sparse_to_string(sparse):
    return "".join((str(s) for s in sparse))


def checksum(data):
    return sum(idx * val for idx, val in enumerate(data))


def day09a(fname):
    dense = parse_data(fname)
    sparse = dense_to_sparse(dense)
    compress = compress_sparse(sparse)
    return checksum(compress)


def dense_to_sparse_b(dense):
    """turns dense into [(v0,l0),(v1,l1)...]
    where v* is the value int or '.'
    l* is the number of values"""
    result = []
    num = 0
    idx, ln = 0, len(dense)
    while idx < ln:
        # add X numbers
        result.append((num, dense[idx]))
        idx += 1
        num += 1
        if idx < ln:
            # add empties
            if dense[idx] > 0:
                result.append((".", dense[idx]))
            idx += 1
    return result


def compress_sparse_b(sparse):
    "compresses the sparse array and returns it"
    # helpers:
    def find_idx(arr, val):
        for idx, v in enumerate(arr):
            if v[0] == val:
                return idx
        return -1

    def find_space(arr, ln):
        for idx, v in enumerate(arr):
            if v[0] == "." and v[1] >= ln:
                return idx
        return -1

    # find the biggest number
    bignum = sparse[-1][0]

    # largest number backwards
    for val in range(bignum, 1, -1):
        # find the number
        idx = find_idx(sparse, val)
        # find a space big enough to hold it
        rec = sparse[idx]
        lnrec = rec[1]
        sidx = find_space(sparse, lnrec)
        if sidx >= 0 and sidx < idx:
            # remove item, but need to consider if the prev/next is also a space:
            sparse[idx] = (".", lnrec)
            if idx + 1 < len(sparse) and sparse[idx + 1][0] == ".":
                # update then remove
                lnrec += sparse[idx + 1][1]
                sparse[idx] = (".", lnrec)
                del sparse[idx + 1]
            if idx > 0 and sparse[idx - 1][0] == ".":
                # update then remove
                lnrec += sparse[idx - 1][1]
                sparse[idx] = (".", lnrec)
                del sparse[idx - 1]
            # two versions of add: exact fit, or fit with space
            lnspc = sparse[sidx][1]
            if lnspc == rec[1]:
                # exact size, replace
                sparse[sidx] = rec
            else:
                # smaller, so we add data & insert a record
                sparse[sidx] = rec
                sparse.insert(sidx + 1, (".", lnspc - rec[1]))
    return sparse


def checksum_b(data):
    total = 0
    tln = 0
    for v, ln in data:
        if v != ".":
            for i in range(ln):
                total += v * (tln + i)
        tln += ln
    return total


def day09b(fname):
    dense = parse_data(fname)
    sparse = dense_to_sparse_b(dense)
    compress = compress_sparse_b(sparse)
    return checksum_b(compress)


################################################################
if __name__ == "__main__":
    print("day09a", day09a("input09.txt"))
    print("day09b", day09b("input09.txt"))

################################################################


def test_parse_data():
    assert parse_data("test09.txt") == [
        2,
        3,
        3,
        3,
        1,
        3,
        3,
        1,
        2,
        1,
        4,
        1,
        4,
        1,
        3,
        1,
        4,
        0,
        2,
    ]


def test_dense_to_sparse():
    assert dense_to_sparse([1, 2, 3, 4, 5]) == [
        0,
        ".",
        ".",
        1,
        1,
        1,
        ".",
        ".",
        ".",
        ".",
        2,
        2,
        2,
        2,
        2,
    ]

    data = dense_to_sparse(parse_data("test09.txt"))
    assert sparse_to_string(data) == "00...111...2...333.44.5555.6666.777.888899"


def test_compress_sparse():
    sparse = [0, ".", ".", 1, 1, 1, ".", ".", ".", ".", 2, 2, 2, 2, 2]
    compress = compress_sparse(sparse)
    assert sparse_to_string(compress) == "022111222"
    # other case is used in day09a


def test_checksum():
    data = [int(a) for a in "0099811188827773336446555566"]
    assert checksum(data) == 1928


def test_day09a():
    assert day09a("test09.txt") == 1928


def test_dense_to_sparse_b():
    data = dense_to_sparse_b(parse_data("test09.txt"))
    assert data == [
        (0, 2),
        (".", 3),
        (1, 3),
        (".", 3),
        (2, 1),
        (".", 3),
        (3, 3),
        (".", 1),
        (4, 2),
        (".", 1),
        (5, 4),
        (".", 1),
        (6, 4),
        (".", 1),
        (7, 3),
        (".", 1),
        (8, 4),
        (9, 2),
    ]


def test_compress_sparse_b():
    data = dense_to_sparse_b(parse_data("test09.txt"))
    compress = compress_sparse_b(data)
    assert compress == [
        (0, 2),
        (9, 2),
        (2, 1),
        (1, 3),
        (7, 3),
        (".", 1),
        (4, 2),
        (".", 1),
        (3, 3),
        (".", 4),
        (5, 4),
        (".", 1),
        (6, 4),
        (".", 5),
        (8, 4),
        (".", 2),
    ]


def test_day09b():
    assert day09b("test09.txt") == 2858
