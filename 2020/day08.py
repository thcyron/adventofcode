from copy import copy


def parse_line(line):
    inst, arg = line.split(" ")
    return inst, int(arg)


def run_once(code, pos, acc):
    try:
        inst, arg = code[pos]
    except IndexError:
        return pos, acc
    if inst == "nop":
        return pos + 1, acc
    if inst == "acc":
        return pos + 1, acc + arg
    if inst == "jmp":
        return pos + arg, acc


def run(code):
    pos, acc = 0, 0
    visited = {pos}
    while True:
        pos, acc = run_once(code, pos, acc)
        if pos in visited:
            return pos, acc
        visited.add(pos)


def swapped_codes(code):
    to_swap = ("jmp", "nop")
    for i, (inst, arg) in enumerate(code):
        if inst in to_swap:
            changed = copy(code)
            new_inst = to_swap[(to_swap.index(inst) + 1) % 2]
            changed[i] = (new_inst, arg)
            yield changed



with open("day08.txt") as f:
    code = [parse_line(line.strip()) for line in f.readlines()]
    print(run(code)[1])
    print(next(acc for pos, acc in (run(c) for c in swapped_codes(code)) if pos == len(code)))
