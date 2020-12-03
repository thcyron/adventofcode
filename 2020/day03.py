from math import prod


def count_trees(forest, slope):
    m = len(forest[0])
    x, y = 0, 0
    trees = 0
    while y < len(forest):
        if forest[y][x % m] == "#":
            trees += 1
        y += slope[0]
        x = (x + slope[1]) % m
    return trees


if __name__ == "__main__":
    forest = [list(_.strip()) for _ in open("day03.txt").readlines()]
    print(count_trees(forest, (1, 3)))
    print(
        prod(
            count_trees(forest, slope)
            for slope in ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1))
        )
    )
