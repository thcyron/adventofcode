from math import prod


with open("day16.txt") as f:
    blocks = f.read().split("\n\n")

def parse_rule(line):
    field, rest = line.split(": ")
    constraints = rest.split(" or ")
    return (field, [[int(_) for _ in c.split("-")] for c in constraints])

rules = [parse_rule(line) for line in blocks[0].split("\n")]

def is_valid(n):
    for _, rule in rules:
        if is_valid_for_rule(n, rule):
            return True
    return False

def is_valid_for_rule(n, rule):
    for r in rule:
        if r[0] <= n <= r[1]:
            return True
    return False

error_rate = 0
valid_tickets = []
mapping = {}

for ticket in blocks[2].split("\n")[1:]:
    numbers = [int(n) for n in ticket.split(",")]
    invalids = [n for n in numbers if not is_valid(n)]
    if invalids:
        error_rate += sum(invalids)
    else:
        valid_tickets.append(numbers)

print(error_rate)

while len(mapping) < len(rules):
    for name, rule in rules:
        if name in mapping.keys():
            continue
        candidates = set()
        for i in range(len(valid_tickets[0])):
            if i in mapping.values():
                continue
            if all(is_valid_for_rule(t[i], rule) for t in valid_tickets):
                candidates.add(i)
        if len(candidates) == 1:
            mapping[name] = list(candidates)[0]

ticket = [int(n) for n in blocks[1].split("\n")[1].split(",")]
print(prod(
    ticket[idx]
    for name, idx in mapping.items()
    if name.startswith("departure")
))
