def parse_pass(p):
    return (to_int(p[0:7], "FB"), to_int(p[7:], "LR"))


def to_int(code, zo):
    return int(code.replace(zo[0], "0").replace(zo[1], "1"), 2)


def seat_id(row, col):
    return row * 8 + col


if __name__ == "__main__":
    with open("day05.txt") as f:
        passes = [parse_pass(_) for _ in f.readlines()]
        ids = {seat_id(r, c) for r, c in passes}
        min_id, max_id = min(ids), max(ids)
        print(max_id)

        all_ids = set(range(min_id, max_id + 1))
        missing = all_ids - ids
        assert len(missing) == 1
        print(list(missing)[0])
