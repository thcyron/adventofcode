def parse_bag_count(x):
    parts = x.split(" ")
    return int(parts[0]), " ".join(parts[1:-1])


def parse_rule(line):
    bag, rest = line.strip().split(" bags contain ", 2)
    if rest == "no other bags.":
        return bag, []
    return bag, [parse_bag_count(_) for _ in rest.split(", ")]


def contains(rules, bag, needle):
    if needle in {_[1] for _ in rules[bag]}:
        return True
    return any([contains(rules, _[1], needle) for _ in rules[bag]])


def count(rules, bag):
    return (
        sum([_[0] for _ in rules[bag]]) +
        sum([_[0] * count(rules, _[1]) for _ in rules[bag]])
    )


with open("day07.txt") as f:
    rules = dict([parse_rule(_) for _ in f.readlines()])
    print(len([bag for bag in rules.keys() if contains(rules, bag, "shiny gold")]))
    print(count(rules, "shiny gold"))
