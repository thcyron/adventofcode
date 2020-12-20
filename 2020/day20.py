from math import sqrt, prod
import itertools
from collections import defaultdict


def parse_tile(data):
    lines = data.split("\n")
    tile_id = int(lines[0].split(" ")[1][0:-1])
    return tile_id, tuple(lines[1:])


def borders(image):
    return (
        image[0],
        "".join([line[-1] for line in image]),
        image[-1],
        "".join([line[0] for line in image]),
    )


def rotate_image(image):
    x = [list(_) for _ in image]
    x = zip(*x[::-1])
    return tuple("".join(_) for _ in x)


def rotate_tile(tile):
    tile_id, image = tile
    return tile_id, rotate_image(image)


def flipped_tiles(tile):
    tile_id, image = tile
    for img in flipped_images(image):
        yield tile_id, img


def flipped_images(image):
    yield tuple(_[::-1] for _ in image)
    yield image[::-1]


def oriented_tiles(tile):
    yield tile
    yield from flipped_tiles(tile)
    for _ in range(3):
        tile = rotate_tile(tile)
        yield tile
        yield from flipped_tiles(tile)


def oriented_images(image):
    yield image
    yield from flipped_images(image)
    for _ in range(3):
        image = rotate_image(image)
        yield image
        yield from flipped_images(image)


def build_square(candidates, a, sq):
    for tile in next_tiles_for(candidates, a, sq):
        sq2 = sq + [tile]
        if len(sq2) == a*a:
            yield sq2
        else:
            tile_ids = {t[0] for t in sq2}
            candidates = {t for t in all_tiles if t[0] not in tile_ids}
            yield from build_square(candidates, a, sq2)


def next_tiles_for(tiles, a, sq):
    i = len(sq)

    if i >= a:
        # must match with tile above
        t = sq[i-a]
        b = borders(t[1])[2]
        tiles &= tiles_by_top[b]

    if i % a > 0:
        # must match with tiles to the left
        t = sq[i-1]
        b = borders(t[1])[1]
        tiles &= tiles_by_left[b]

    return tiles


def stitch(sq, a):
    image = []
    for srow in range(a):
        for trow in range(1, 9):
            full_line = ""
            for scol in range(a):
                tile = sq[a*srow + scol]
                line = tile[1][trow]
                full_line += line[1:-1]
            image.append(full_line)
    return image


MONSTER = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """


def calculate_monster_positions():
    for y, line in enumerate(MONSTER.split("\n")):
        for x, c in enumerate(line):
            if c == "#":
                yield (x,y)


monster_positions = list(calculate_monster_positions())


def check_monster(img, x, y):
    for pos in monster_positions:
        if img[y + pos[1]][x + pos[0]] != "#":
            return False
    return True


def replace_monster(image, x, y):
    updated = list(image)
    for pos in monster_positions:
        line = updated[y + pos[1]]
        line = line[:x + pos[0]] + "O" + line[x+pos[0]+1:]
        updated[y + pos[1]] = line
    return updated


def find_monsters(image):
    mx = max(_[0] for _ in monster_positions)
    my = max(_[1] for _ in monster_positions)
    monsters = 0

    for y in range(0, len(image) - my + 1):
        for x in range(0, len(image[0]) - mx + 1):
            if check_monster(image, x, y):
                monsters += 1
                image = replace_monster(image, x, y)

    return monsters, image


with open("day20.txt") as f:
    tiles = {parse_tile(block.strip()) for block in f.read().split("\n\n")}

all_tiles = set(itertools.chain.from_iterable(oriented_tiles(t) for t in tiles))

tiles_by_top = defaultdict(set)
tiles_by_left = defaultdict(set)

for t in all_tiles:
    bs = borders(t[1])
    tiles_by_top[bs[0]].add(t)
    tiles_by_left[bs[3]].add(t)

a = int(sqrt(len(tiles)))
sq = next(build_square(all_tiles, a, []))
print(prod(sq[i][0] for i in (0, a-1, -a, -1)))

image = stitch(sq, a)

final_image = next(
    img for n, img in
    (find_monsters(img) for img in oriented_images(image))
    if n > 0
)

print(sum(1 for line in final_image for c in line if c == "#"))
