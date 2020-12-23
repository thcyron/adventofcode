class Cup:
    def __init__(self, label):
        self.label = label
        self.next = None
        self.prev = None


def take(cup, n):
    for _ in range(n):
        yield cup
        cup = cup.next


def pick(cup):
    a = cup.next
    b = a.next
    c = b.next
    cup.next = c.next
    cup.next.prev = cup
    a.prev = None
    c.next = None
    return [a,b,c]


def play(cups, rounds):
    cup_by_label = {cup.label: cup for cup in cups}
    cup = cups[0]

    for _ in range(rounds):
        picks = pick(cup)
        picked_labels = [cup.label for cup in picks]

        dest = cup.label - 1
        while dest in picked_labels or dest == 0:
            if dest == 0:
                dest = len(cups)
            else:
                dest = dest - 1

        dest_cup = cup_by_label[dest]
        picks[-1].next = dest_cup.next
        dest_cup.next = picks[0]
        cup = cup.next

    return cup_by_label[1]


def cups_for(labels):
    cups = [Cup(int(label)) for label in labels]
    for i, cup in enumerate(cups):
        cup.next = cups[(i + 1) % len(labels)]
        cup.prev = cups[(i - 1) % len(labels)]
    return cups


INPUT = "326519478"

cups = cups_for(INPUT)
cup = play(cups, rounds=100)
print("".join(str(cup.label) for cup in list(take(cup, len(cups)))[1:]))

cups = cups_for(list(INPUT) + list(range(len(INPUT) + 1, 1_000_000 + 1)))
cup = play(cups, rounds=10_000_000)
print(cup.next.label * cup.next.next.label)
