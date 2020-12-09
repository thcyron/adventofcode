import itertools


def part1(numbers):
    for i in range(25, len(numbers)):
        pre = numbers[i-25:i]
        number = numbers[i]
        if not any(s == number for s in map(sum, itertools.combinations(pre, 2))):
            return number


def part2(numbers, number):
    for i in range(len(numbers) - 1):
        for j in range(i+1, len(numbers)):
            s = sum(numbers[i:j])
            if s == number:
                return min(numbers[i:j]) + max(numbers[i:j])
            if s > number:
                break


with open("day09.txt") as f:
    numbers = [int(line.strip()) for line in f.readlines()]
    number = part1(numbers)
    print(number)
    print(part2(numbers, number))

