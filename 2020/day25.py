PUBLIC_KEY_CARD = 13316116
PUBLIC_KEY_DOOR = 13651422


def find_loop_size(target, sn=7):
    ls = 1
    n = 1
    while True:
        n = (n * sn) % 20201227
        if n == target:
            return ls
        ls += 1


def calculate_encryption_key(public_key, loop_size):
    key = 1
    for _ in range(loop_size):
        key = (key * public_key) % 20201227
    return key


card_loop_size = find_loop_size(PUBLIC_KEY_CARD)
door_loop_size = find_loop_size(PUBLIC_KEY_DOOR)

print(calculate_encryption_key(PUBLIC_KEY_DOOR, card_loop_size))
