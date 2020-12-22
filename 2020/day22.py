with open("day22.txt") as f:
    blocks = f.read().split("\n\n")
    decks = [tuple(int(n) for n in block.split("\n")[1:]) for block in blocks]


def play(p1, p2):
    while p1 and p2:
        c1, c2 = p1[0], p2[0]
        p1, p2 = p1[1:], p2[1:]
        if c1 > c2:
            p1 += (c1, c2)
        else:
            p2 += (c2, c1)
    return p1 or p2


def rplay(p1, p2):
    games = set()

    while p1 and p2:
        if (p1,p2) in games:
            return 1, p1
        games.add((p1,p2))

        c1, c2 = p1[0], p2[0]
        p1, p2 = p1[1:], p2[1:]
        if len(p1) >= c1 and len(p2) >= c2:
            q1, q2 = p1[:c1], p2[:c2]
            result = rplay(q1, q2)
            if result[0] == 1:
                p1 += (c1, c2)
            else:
                p2 += (c2, c1)
        else:
            if c1 > c2:
                p1 += (c1, c2)
            else:
                p2 += (c2, c1)

    if p1:
        return 1, p1
    else:
        return 2, p2


p1, p2 = decks
print(sum((i+1) * n for i, n in enumerate(reversed(play(p1, p2)))))
print(sum((i+1) * n for i, n in enumerate(reversed(rplay(p1, p2)[1]))))
