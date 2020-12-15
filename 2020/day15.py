numbers = [9,3,1,0,8,4]
indices = {n: i for i, n in enumerate(numbers)}
stops = [2020, 30000000]

i = len(numbers) - 1
n = numbers[i]

while stops:
    try:
        m = i - indices[n]
    except KeyError:
        m = 0

    indices[n] = i
    i += 1

    if i == stops[0]:
        print(n)
        stops.pop(0)

    n = m
