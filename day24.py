import pytest
import math
from helpers import load_tokens
import sys

""" Looks familiar, circuit simulation.
PartB is not really computable, its debugging.
The logic is adding 2 x 45 bit numbers & it doesn't work.
We need to swap lines.
note: https://www.build-electronic-circuits.com/wp-content/uploads/2022/10/fullAdder2-1024x520.png
is the implementation, you you need to look at X10,Y10 & the carry in to check it
"""


def parse_data(fname):
    "return (dict(input:value),[(inA,AND/OR/XOR,inB,out)])"
    inputs = {}
    wires = []

    for tokens in load_tokens(fname):
        if len(tokens) == 2:
            inp = tokens[0].strip(":")
            value = int(tokens[1])
            inputs[inp] = value
        elif len(tokens) == 5:
            wires.append((tokens[0], tokens[1], tokens[2], tokens[4]))

    return inputs, wires


def process(inputs, wires):
    "processed all & returns all the nodes"
    nodes = dict(inputs)
    processing = True
    triggered = []
    while processing:
        processing = False
        # look through all the wires & trigger
        # must have both inputs set & not triggered
        for idx, (inA, op, inB, out) in enumerate(wires):
            if idx in triggered:
                continue
            if inA in nodes and inB in nodes:
                dataA, dataB = nodes[inA], nodes[inB]
                if out in nodes:
                    print(f"warning nodes[{out}] is set to {nodes[out]}")
                if op == "AND":
                    nodes[out] = dataA & dataB
                elif op == "OR":
                    nodes[out] = dataA | dataB
                else:
                    nodes[out] = dataA ^ dataB
                triggered.append(idx)
                processing = True

    return nodes


def get_value(nodes):
    "turn z00... into an int"
    value = 0
    idx = 0
    while True:
        key = f"z{idx:02d}"
        if key not in nodes:
            break
        if nodes[key] == 1:
            value += 2 ** idx
        idx += 1
    return value


def day24a(fname):
    inputs, wires = parse_data(fname)
    nodes = process(inputs, wires)
    ##    print(nodes)
    # turn z00... into an int
    return get_value(nodes)


def test_process(wires, x, y, ioi):
    inputs = {}

    def set_value(prefix, num):
        for idx in range(45):
            key = f"{prefix}{idx:02d}"
            v = num % 2
            inputs[key] = v
            num //= 2

    set_value("x", x)
    set_value("y", y)
    nodes = process(inputs, wires)
    val = get_value(nodes)
    if x + y == val:
        return True
    print(f"{x} + {y} = {val} incorrect")
    # diagnostics
    r = "X:"
    for i in range(44, -1, -1):
        r += str(nodes[f"x{i:02d}"])
    print(r)
    r = "Y:"
    for i in range(44, -1, -1):
        r += str(nodes[f"y{i:02d}"])
    print(r)
    r = "Z:"
    for i in range(44, -1, -1):
        r += str(nodes[f"z{i:02d}"])
    print(r)
    # items of interest
    for text, key in ioi:
        print(f"{text}({key}): {nodes[key]}")
    return False


def generate_items_of_interest(wires, starts):
    result = starts[:]
    strs = []
    finish = False
    while not finish:
        finish = True
        for (inA, op, inB, out) in wires:
            if inA in result and inB in result and out not in result:
                result.append(out)
                strs.append(f"{inA} {op} {inB} -> {out}")
                finish = False

    return [(r, r) for r in result], strs


def repair(wires, a, b):
    "swaps a&b"
    for idx, (inA, op, inB, out) in enumerate(wires):
        if out == a:
            wires[idx] = (inA, op, inB, b)
        if out == b:
            wires[idx] = (inA, op, inB, a)


def day24b(fname):
    """Not solving this, just debugging this.
    going to try adding 000+000, 000+001 and so on.
    until it breaks, then adding a manual fix & moving on
    """
    inputs, wires = parse_data(fname)

    repair(wires, "z10", "vcf")
    ioi, strs = generate_items_of_interest(wires, ["x09", "y09", "jgj", "x10", "y10"])
    if not test_process(wires, 512, 512, ioi):
        print("rules")
        for s in strs:
            print(s)
        return

    repair(wires, "z17", "fhg")
    ioi, strs = generate_items_of_interest(wires, ["x16", "y16", "rfv", "x17", "y17"])
    if not test_process(wires, 65536, 65536, ioi):
        print("rules")
        for s in strs:
            print(s)
        return

    repair(wires, "dvb", "fsq")
    ioi, strs = generate_items_of_interest(wires, ["x35", "y35", "rfv", "x36", "y36"])
    if not test_process(wires, 2 ** 35, 2 ** 35, ioi):
        print("rules")
        for s in strs:
            print(s)
        return

    repair(wires, "z39", "tnc")
    ioi, strs = generate_items_of_interest(wires, ["x38", "y38", "hkj", "x39", "y39"])
    if not test_process(wires, 2 ** 38, 2 ** 38, ioi):
        print("rules")
        for s in strs:
            print(s)
        return

    # simple & quick test for each bit in turn
    for x in range(45):
        if test_process(wires, 2 ** x, 2 ** x, []) == False:
            print("issue with bit", x)
            break
        sys.stdout.write(".")
        sys.stdout.flush()

    print()
    result = ["z10", "vcf", "z17", "fhg", "dvb", "fsq", "z39", "tnc"]
    result.sort()
    return ",".join(result)


################################################################
if __name__ == "__main__":
    ##    print("day24a", day24a("input24.txt"))
    print("day24b", day24b("input24.txt"))


################################################################


def test_parse_data():
    inputs, wires = parse_data("test24a.txt")
    assert len(inputs) == 6
    assert inputs["x00"] == 1
    assert inputs["y02"] == 0

    assert len(wires) == 3
    assert wires[0] == ("x00", "AND", "y00", "z00")
    assert wires[-1] == ("x02", "OR", "y02", "z02")


def test_process():
    inputs, wires = parse_data("test24a.txt")
    nodes = process(inputs, wires)
    print(nodes)
    assert nodes["z00"] == 0
    assert nodes["z01"] == 0
    assert nodes["z02"] == 1


def test_day24a():
    assert day24a("test24a.txt") == 4
    assert day24a("test24b.txt") == 2024
