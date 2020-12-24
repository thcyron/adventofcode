def follow_once(p, d):
    x, y = p
    if d == "e":
        x += 1
    elif d == "se":
        if y % 2 == 1:
            x += 1
        y += 1
    elif d == "sw":
        if y % 2 == 0:
            x -= 1
        y += 1
    elif d == "w":
        x -= 1
    elif d == "nw":
        if y % 2 == 0:
            x -= 1
        y -= 1
    elif d == "ne":
        if y % 2 == 1:
            x += 1
        y -= 1
    else:
        raise RuntimeError("invalid directions")
    return x, y


def follow(direction):
    x, y = 0, 0
    while direction:
        if direction[0] in ("e","w"):
            x, y = follow_once((x,y), direction[0])
            direction = direction[1:]
        else:
            x, y = follow_once((x,y), direction[:2])
            direction = direction[2:]
    return x, y


def neighbors(p):
    for d in ("e", "se", "sw", "w", "nw", "ne"):
        yield follow_once(p, d)


def day(tiles):
    for p in list(tiles.keys()):
        for n in neighbors(p):
            if n not in tiles:
                tiles[n] = "w"

    changes = {}

    for p, color in tiles.items():
        colors = [tiles.get(n, "w") for n in neighbors(p)]
        blacks = sum(1 for c in colors if c == "b")
        if color == "b":
            if blacks == 0 or blacks > 2:
                changes[p] = "w"
        else:
            if blacks == 2:
                changes[p] = "b"

    for p, c in changes.items():
        tiles[p] = c


with open("day24.txt") as f:
    directions = [line.strip() for line in f.readlines()]

tiles = {}

for direction in directions:
    p = follow(direction)
    c = tiles.get(p, "w")
    if c == "w":
        tiles[p] = "b"
    else:
        tiles[p] = "w"

print(sum(1 for _, t in tiles.items() if t == "b"))

for _ in range(100):
    day(tiles)

print(sum(1 for _, t in tiles.items() if t == "b"))
