from itertools import combinations
from math import prod


def day01(expenses, count):
    for c in combinations(expenses, count):
        if sum(c) == 2020:
            return prod(c)


if __name__ == "__main__":
    expenses = [int(_) for _ in open("day01.txt").readlines()]
    print(day01(expenses, 2))
    print(day01(expenses, 3))
