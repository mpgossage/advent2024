import pytest
import math
from helpers import load_tokens
from time import perf_counter as clock
import sys

""" graph time.
Little unsure on get_largest_lan() but it worked ok.
"""


def parse_data(fname):
    "return dict(a:[b,c,d]) of connections (a<->b), both ways"

    def graph_add(g, a, b):
        g[a] = g.get(a, []) + [b]

    graph = {}
    for a, b in load_tokens(fname, "-"):
        graph_add(graph, a, b)
        graph_add(graph, b, a)

    return graph


def find_lan3(graph, node):
    "returns all 3 node LAN's connected to 'node'"
    connected = graph[node]
    lnconn = len(connected)
    result = []
    for i in range(lnconn):
        for j in range(i + 1, lnconn):
            na, nb = connected[i], connected[j]
            # if na&nb are connected its a lan
            if nb in graph[na]:
                result.append((node, na, nb))
    return result


def day23a(fname):
    # spotted trick: get nodes starting with T... and just check them
    # need to check for dups, using set for that
    graph = parse_data(fname)
    result = []
    for n in graph.keys():
        if n[0] != "t":
            continue
        lans = find_lan3(graph, n)
        for l in lans:
            # turn lan into a set so we can ignore the order
            l = set(l)
            if l not in result:
                result.append(l)
    return len(result)


def get_largest_lan(graph):
    "returns the largest lan"
    is_linked = lambda a, b: a in graph[b]
    largest = set()
    for n, connected in graph.items():
        lenc = len(connected)
        for c in connected:
            # find largest lan with n & c
            lan = set([n, c])
            has_added = True
            while has_added:
                has_added = False
                for c2 in connected:
                    if c2 in lan:
                        continue
                    linked_to_all = True
                    for l in lan:
                        if is_linked(l, c2) == False:
                            linked_to_all = False
                            break
                    if linked_to_all:
                        lan.add(c2)
                        has_added = True
                        break
            if len(lan) > len(largest):
                print("found", lan)
                largest = lan
    return largest


def get_lan_password(lan):
    lan = list(lan)
    lan.sort()
    return ",".join(lan)


def day23b(fname):
    graph = parse_data(fname)
    lan = get_largest_lan(graph)
    return get_lan_password(lan)


################################################################
if __name__ == "__main__":
    print("day23a", day23a("input23.txt"))
    print("day23b", day23b("input23.txt"))


################################################################


def test_parse_data():
    graph = parse_data("test23.txt")
    assert "kh" in graph["tc"]
    assert "tc" in graph["kh"]
    assert "td" in graph["yn"]
    assert "yn" in graph["td"]


def test_find_lan3():
    graph = parse_data("test23.txt")
    ta_lan = find_lan3(graph, "ta")
    assert len(ta_lan) == 3
    in_lan = lambda lst, a, b, c: (a, b, c) in lst or (a, c, b) in lst
    assert in_lan(ta_lan, "ta", "co", "de")
    assert in_lan(ta_lan, "ta", "co", "ka")


def test_day23a():
    assert day23a("test23.txt") == 7


def test_get_largest_lan():
    graph = parse_data("test23.txt")
    lan = get_largest_lan(graph)


def test_day23b():
    assert day23b("test23.txt") == "co,de,ka,ta"
