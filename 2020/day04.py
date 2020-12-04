import re


def parse_passport(data):
    fields = {}
    for line in data.strip().split("\n"):
        for kv in line.strip().split(" "):
            k, v = kv.split(":")
            fields[k] = v
    return fields


def parse_passports(data):
    return [parse_passport(_) for _ in data.split("\n\n")]


FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}


def validate_fields(passport):
    missing = FIELDS - passport.keys()
    return len(missing) == 0 or missing == {"cid"}


def validate_byr(passport):
    try:
        return 1920 <= int(passport["byr"]) <= 2002
    except ValueError:
        return False


def validate_iyr(passport):
    try:
        return 2010 <= int(passport["iyr"]) <= 2020
    except ValueError:
        return False


def validate_eyr(passport):
    try:
        return 2020 <= int(passport["eyr"]) <= 2030
    except ValueError:
        return False


def validate_hgt(passport):
    m = re.match(r"^(\d+)(in|cm)$", passport["hgt"])
    if m:
        h = int(m[1])
        if m[2] == "in":
            return 59 <= h <= 76
        if m[2] == "cm":
            return 150 <= h <= 193
    return False


def validate_hcl(passport):
    return bool(re.match(r"^#[a-f0-9]{6}$", passport["hcl"]))


EYECOLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def validate_ecl(passport):
    return passport["ecl"] in EYECOLORS


def validate_pid(passport):
    return bool(re.match(r"^[0-9]{9}$", passport["pid"]))


def is_valid(passport, validations):
    return all(v(passport) for v in validations)


if __name__ == "__main__":
    with open("day04.txt") as f:
        passports = parse_passports(f.read())
        print(len([p for p in passports if validate_fields(p)]))
        print(len([p for p in passports if is_valid(p, (
            validate_fields,
            validate_byr,
            validate_iyr,
            validate_eyr,
            validate_hgt,
            validate_hcl,
            validate_ecl,
            validate_pid,
        ))]))
