def parse_pass(p):
    return int(p.translate(str.maketrans("FBLR", "0101")), 2)


if __name__ == "__main__":
    with open("day05.txt") as f:
        ids = {parse_pass(_) for _ in f.readlines()}
        min_id, max_id = min(ids), max(ids)
        print(max_id)

        all_ids = set(range(min_id, max_id + 1))
        missing = all_ids - ids
        assert len(missing) == 1
        print(list(missing)[0])
