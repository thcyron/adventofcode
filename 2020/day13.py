from math import ceil, prod, gcd
from functools import reduce


# Chinese remainder functions taken from:
# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


with open("day13.txt") as f:
    notes = [line.strip() for line in f]

    earliest = int(notes[0])
    ids = [int(bus) for bus in notes[1].split(",") if bus != "x"]
    print(
        prod(
            sorted(
                [(bus, bus*ceil(earliest / bus) - earliest) for bus in ids],
                key=lambda _: _[1],
            )[0],
        ),
    )

    params = [
        (int(b), int(b)-i)
        for i, b in enumerate(notes[1].split(","))
        if b != "x"
    ]
    print(chinese_remainder(
        [_[0] for _ in params],
        [_[1] for _ in params],
    ))
