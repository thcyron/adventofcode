import re


def masked(n, mask):
    for i in range(len(mask)):
        if mask[-1-i] == "0":
            n &= ~(1 << i)
        elif mask[-1-i] == "1":
            n |= (1 << i)
    return n


def addresses(addr, mask):
    def gen(a, idx):
        for i in range(idx, len(mask)):
            if mask[-1-i] == "1":
                a |= (1 << i)
            elif mask[-1-i] == "X":
                yield from gen(a & ~(1 << i), i + 1)
                yield from gen(a | (1 << i), i + 1)
                return
        yield a

    yield from gen(addr, 0)


RE_ASSIGNMENT = re.compile(r"mem\[(\d+)\] = (\d+)")

def assignment(line):
    m = RE_ASSIGNMENT.match(line)
    return int(m.group(1)), int(m.group(2))


with open("day14.txt") as f:
    lines = [line.strip() for line in f]

mem = {}
for line in lines:
    if line.startswith("mask"):
        mask = line.split(" ")[2]
    else:
        addr, value = assignment(line)
        mem[addr] = masked(value, mask)
print(sum(mem.values()))

mem = {}
for line in lines:
    if line.startswith("mask"):
        mask = line.split(" ")[2]
    else:
        addr, value = assignment(line)
        for a in addresses(addr, mask):
            mem[a] = value
print(sum(mem.values()))
