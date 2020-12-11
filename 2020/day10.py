from collections import Counter
from math import prod
from functools import cache


with open("day10.txt") as f:
    ratings = sorted([int(line.strip()) for line in f])
    ratings = [0] + ratings + [ratings[-1] + 3]

    diffs = [b-a for a, b in zip(ratings, ratings[1:])]
    print(prod(Counter(diffs).values()))

    reachable = {}
    for i in range(len(ratings) - 1):
        j = i + 1
        d = 0
        r = set()
        while True:
            try:
                d += diffs[j-1]
            except IndexError:
                break
            if d <= 3:
                r.add(ratings[j])
                j += 1
            else:
                break
        reachable[ratings[i]] = r

    @cache
    def dfs(n):
        if n == ratings[-1]:
            return 1
        return sum(map(dfs, reachable[n]))

    print(dfs(0))
