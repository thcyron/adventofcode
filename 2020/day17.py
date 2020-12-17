grid3 = {}
grid4 = {}

with open("day17.txt") as f:
    for y, line in enumerate(f.readlines()):
        for x, s in enumerate(line.strip()):
            grid3[(x,y,0)] = s
            grid4[(x,y,0,0)] = s

def neigh(grid, pos, dim):
    for x in (pos[0] - 1, pos[0], pos[0] + 1):
        for y in (pos[1] - 1, pos[1], pos[1] + 1):
            for z in (pos[2] - 1, pos[2], pos[2] + 1):
                if dim == 3:
                    if (x,y,z) != pos:
                        yield (x,y,z)
                else:
                    for w in (pos[3] - 1, pos[3], pos[3] + 1):
                        if (x,y,z,w) != pos:
                            yield (x,y,z,w)

def run(grid, dim):
    changes = {}

    for p in {p2 for p in grid for p2 in neigh(grid, p, dim)}:
        active_neighbors = [n for n in neigh(grid, p, dim) if grid.get(n) == "#"]
        if grid.get(p) == "#":
            if len(active_neighbors) not in (2,3):
                changes[p] = "."
        else:
            if len(active_neighbors) == 3:
                changes[p] = "#"

    for p, s in changes.items():
        grid[p] = s

for _ in range(6):
    run(grid3, 3)
    run(grid4, 4)

print(sum(1 for s in grid3.values() if s == "#"))
print(sum(1 for s in grid4.values() if s == "#"))
