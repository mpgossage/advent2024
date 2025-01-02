import pytest
import math
from helpers import load_lines
from time import perf_counter as clock
import sys

""" Recognise this kind of puzzle:
part A 2000 iterations, part B a few gazillion.
Part A solved in 9.8 seconds
Part B looks much more time consuming in a different direction, but its still bad
(approx 10000 times slower)

Early tests 10K iterations in 60 seconds.
Redesigned algorithm and got result in 17 seconds, but its too high (2288).
Issue found: it double counted a sequence
"""


def iterate(num):
    mix = lambda a, b: a ^ b
    prune = lambda a: a % 16777216

    num = prune(mix(num, num * 64))
    num = prune(mix(num, num // 32))
    num = prune(mix(num, num * 2048))
    return num


def day22a(fname, cycles):
    total = 0
    start = clock()
    for line in load_lines(fname):
        num = int(line)
        for n in range(cycles):
            num = iterate(num)
        print(f"{line} {num} {clock()-start:.3f}")
        total += num
    return total


def get_price_list(num):
    "returns the list of prices (0..9)"
    result = [num % 10]
    for _ in range(2000):
        num = iterate(num)
        result.append(num % 10)
    return result


# ignore
def get_price_if_match(prices, seq):
    for i in range(len(prices) - 4):
        if (
            prices[i + 1] - prices[i] == seq[0]
            and prices[i + 2] - prices[i + 1] == seq[1]
            and prices[i + 3] - prices[i + 2] == seq[2]
            and prices[i + 4] - prices[i + 3] == seq[3]
        ):
            return prices[i + 4]
    return 0


# ignore
def gen_pattern():
    "returns generator which gives a,b,c,d"
    # simple optimisation a+b+c+d >=-9 and <=9
    # so we can control the ranges accordingly

    for a in range(-9, 10):
        mn, mx = max(-9, -9 - a), min(9, 9 - a)
        for b in range(mn, mx + 1):
            assert -9 <= a + b <= 9
            mn, mx = max(-9, -9 - a - b), min(9, 9 - a - b)
            for c in range(mn, mx + 1):
                assert -9 <= a + b + c <= 9
                mn, mx = max(0, -9 - a - b - c), min(9, 9 - a - b - c)
                for d in range(mn, mx):
                    yield a, b, c, d


# ignore
def _day22b(fname):
    start = clock()
    prices = []
    for line in load_lines(fname):
        prices.append(get_price_list(int(line)))
    print(f"read {len(prices)} prices in {clock()-start:.3f} seconds")
    start = clock()
    count = 0
    best, bscore = None, 0
    for seq in gen_pattern():
        score = 0
        for p in prices:
            score += get_price_if_match(p, seq)
        if score > bscore:
            best, bscore = seq, score
            print(f"found {seq} {score}")
        count += 1
        if count % 1000 == 0:
            print(f"iteration {count} in {clock()-start:.3f} seconds")
    return bscore


def day22b(fname):
    """flipping problem on head.
    Rather than iterate on all the possible sequences (~20^4).
    Just list out the scores and the sequence that created them.
    """
    scores = {}
    start = clock()
    for line in load_lines(fname):
        prices = get_price_list(int(line))
        sequences = set()
        for i in range(len(prices) - 4):
            a, b, c, d, e = (
                prices[i],
                prices[i + 1],
                prices[i + 2],
                prices[i + 3],
                prices[i + 4],
            )
            delta = (b - a, c - b, d - c, e - d)
            # stop double counting
            if delta in sequences:
                continue
            sequences.add(delta)

            sc = scores.get(delta, 0)
            scores[delta] = sc + e
        sys.stdout.write(".")
        sys.stdout.flush()
    print(f"\ntotal scores {len(scores)} in {clock()-start:.3f} seconds")

    return max(scores.values())


################################################################
if __name__ == "__main__":
    ##    print("day22a", day22a("input22.txt",2000))
    print("day22b", day22b("input22.txt"))


################################################################


def test_iterate():
    assert 15887950 == iterate(123)
    assert 16495136 == iterate(15887950)
    assert 527345 == iterate(16495136)
    assert 704524 == iterate(527345)
    assert 1553684 == iterate(704524)
    assert 12683156 == iterate(1553684)
    assert 11100544 == iterate(12683156)
    assert 12249484 == iterate(11100544)
    assert 7753432 == iterate(12249484)
    assert 5908254 == iterate(7753432)


def test_day22a():
    assert day22a("test22.txt", 2000) == 37327623


def test_get_price_list():
    result = get_price_list(123)
    assert result[0] == 3
    assert result[1] == 0
    assert result[2] == 6
    assert result[3] == 5
    assert result[4] == 4
    assert result[5] == 4
    assert result[6] == 6
    assert result[7] == 4
    assert result[8] == 4
    assert result[9] == 2


def test_get_price_if_match():
    prices = get_price_list(123)
    assert get_price_if_match(prices, (-3, 6, -1, -1)) == 4
    assert get_price_if_match(prices, (-1, -1, 0, 2)) == 6


def test_day22b():
    # initally failed, giving bigger result than
    # 23 from -2,1,-1,3
    assert day22b("test22b.txt") == 23
