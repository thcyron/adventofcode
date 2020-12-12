BEARINGS = "NESW"

def move(inst, pos):
    a, v = inst
    x, y, b = pos

    if a == "N":
        return (x, y+v, b)
    if a == "S":
        return (x, y-v, b)
    if a == "E":
        return (x+v, y, b)
    if a == "W":
        return (x-v, y, b)
    if a == "L":
        turns = v // 90
        b2 = BEARINGS[(BEARINGS.index(b) - turns) % 4]
        return (x, y, b2)
    if a == "R":
        turns = v // 90
        b2 = BEARINGS[(BEARINGS.index(b) + turns) % 4]
        return (x, y, b2)
    if a == "F":
        if b == "N":
            return (x, y+v, b)
        if b == "S":
            return (x, y-v, b)
        if b == "E":
            return (x+v, y, b)
        if b == "W":
            return (x-v, y, b)


def move2(inst, pos):
    a, v = inst
    sx, sy, wx, wy = pos

    if a == "N":
        return (sx, sy, wx, wy+v)
    if a == "S":
        return (sx, sy, wx, wy-v)
    if a == "E":
        return (sx, sy, wx+v, wy)
    if a == "W":
        return (sx, sy, wx-v, wy)
    if a == "L":
        while v > 0:
            wx, wy = -wy, wx
            v -= 90
        return (sx, sy, wx, wy)
    if a == "R":
        while v > 0:
            wx, wy = wy, -wx
            v -= 90
        return (sx, sy, wx, wy)
    if a == "F":
        return (sx + v*wx, sy + v*wy, wx, wy)


def distance(pos):
    return sum(map(abs, pos[0:2]))


with open("day12.txt") as f:
    instructions = [(line[0], int(line[1:].strip())) for line in f]

    pos = (0, 0, "E")
    for inst in instructions:
        pos = move(inst, pos)
    print(distance(pos))

    pos = (0, 0, 10, 1)
    for inst in instructions:
        pos = move2(inst, pos)
    print(distance(pos))
