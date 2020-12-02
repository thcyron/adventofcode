def parse_line(line):
    parts = line.strip().split()
    counts = parts[0].split("-")
    letter = parts[1].split(":")[0]
    password = parts[2]
    return {
        "a": int(counts[0]),
        "b": int(counts[1]),
        "letter": letter,
        "password": password,
    }


def is_valid_old(line):
    count = line["password"].count(line["letter"])
    return line["a"] <= count <= line["b"]


def is_valid_new(line):
    a = line["password"][line["a"] - 1]
    b = line["password"][line["b"] - 1]
    return (a == line["letter"]) != (b == line["letter"])


if __name__ == "__main__":
    lines = [parse_line(_) for _ in open("day02.txt").readlines()]
    print(len([1 for _ in lines if is_valid_old(_)]))
    print(len([1 for _ in lines if is_valid_new(_)]))
