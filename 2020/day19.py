with open("day19.txt") as f:
    blocks = f.read().strip().split("\n\n")

def parse_rules(data):
    rules = {}
    for line in data.split("\n"):
        number, rest = line.split(": ")
        if rest.startswith('"'):
            rules[int(number)] = rest[1]
        else:
            options = rest.split(" | ")
            rules[int(number)] = [[int(n) for n in option.split(" ")] for option in options]
    return rules

def check(message, rules, rule):
    if not rule:
        return message == ""
    if not message:
        return False

    r0 = rule[0]

    if isinstance(rules[r0], str):
        if message[0] != rules[r0]:
            return False
        return check(message[1:], rules, rule[1:])

    for rr in rules[r0]:
        new = rr + rule[1:]
        if check(message, rules, new):
            return True

    return False

rules = parse_rules(blocks[0])
messages = blocks[1].split("\n")

res = lambda: sum(1 for message in messages if check(message, rules, rules[0][0]))

print(res())
rules[8] = [[42], [42,8]]
rules[11] = [[42,31], [42,11,31]]
print(res())
