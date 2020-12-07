def parse_bag_count(x):
    parts = x.split(" ")
    return " ".join(parts[1:-1]), int(parts[0])


def parse_rule(line):
    bag, rest = line.strip().split(" bags contain ", 2)
    if rest == "no other bags.":
        return bag, {}
    return bag, dict([parse_bag_count(_) for _ in rest.split(", ")])


def contains(rules, bag, needle):
    return (
        needle in rules[bag].keys() or
        any([contains(rules, b, needle) for b in rules[bag].keys()])
    )


def count(rules, bag):
    return (
        sum(rules[bag].values()) +
        sum([c * count(rules, b) for b, c in rules[bag].items()])
    )


with open("day07.txt") as f:
    rules = dict([parse_rule(_) for _ in f.readlines()])
    print(len([bag for bag in rules.keys() if contains(rules, bag, "shiny gold")]))
    print(count(rules, "shiny gold"))
