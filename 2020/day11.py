from copy import deepcopy
from itertools import product


def adjacent(plan, row, col, loop=False):
    for dr, dc in product([-1,0,1], repeat=2):
        if dr == 0 and dc == 0:
            continue
        r = row + dr
        c = col + dc
        while 0 <= r < len(plan) and 0 <= c < len(plan[0]):
            if plan[r][c] != ".":
                yield plan[r][c]
                break
            else:
                if loop:
                    c += dc
                    r += dr
                else:
                    break


def run(plan, loop, nocc):
    new_plan = deepcopy(plan)
    for r in range(len(plan)):
        for c in range(len(plan[r])):
            seat = plan[r][c]
            adj = list(adjacent(plan, r, c, loop=loop))

            if seat == "L":
                if "#" not in adj:
                    new_plan[r][c] = "#"
            elif seat == "#":
                if len([_ for _ in adj if _ == "#"]) >= nocc:
                    new_plan[r][c] = "L"

    return new_plan


with open("day11.txt") as f:
    plan = [list(line.strip()) for line in f]

    for (loop, nocc) in ((False, 4), (True, 5)):
        pl = deepcopy(plan)
        while True:
            pl2 = run(pl, loop=loop, nocc=nocc)
            if pl2 == pl:
                break
            pl = pl2
        print(len([1 for row in pl for seat in row if seat == "#"]))
