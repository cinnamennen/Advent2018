from collections import Counter


def contain_two(f: list):
    return 2 in Counter(f).values()


def contain_three(f: list):
    return 3 in Counter(f).values()


two = three = 0

with open('a.txt') as f:
    for line in f.readlines():
        strip = list(line.strip())
        if contain_two(strip):
            two += 1

        if contain_three(strip):
            three += 1

print(f'{two} x {three} = {two * three}')
