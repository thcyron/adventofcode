def parse_pass(p):
    for a, b in ("F0", "B1", "L0", "R1"):
        p = p.replace(a, b)
    return int(p, 2)


if __name__ == "__main__":
    with open("day05.txt") as f:
        ids = {parse_pass(_) for _ in f.readlines()}
        min_id, max_id = min(ids), max(ids)
        print(max_id)

        all_ids = set(range(min_id, max_id + 1))
        missing = all_ids - ids
        assert len(missing) == 1
        print(list(missing)[0])
