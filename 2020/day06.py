with open("day06.txt") as f:
    groups = [[set(person) for person in group.split("\n")] for group in f.read().strip().split("\n\n")]
    print(sum([len(answers) for group in groups for answers in set.union(*group)]))
    print(sum([len(answers) for group in groups for answers in set.intersection(*group)]))
