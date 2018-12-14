import pprint
from typing import List, Tuple

pp = pprint.PrettyPrinter(indent=4)

file = 'x.txt'
data = [_.strip() for _ in open(file).readlines()]


def print_score(s: List[int], x: int, y: int):
    to_print = [' {} '.format(d) for d in s]
    to_print[x] = '({})'.format(s[x])
    to_print[y] = '[{}]'.format(s[y])
    print("".join(to_print))




def new_score(s: List[int], x: int, y: int) -> Tuple[int, int]:
    combined = s[x] + s[y]

    new_recipies = list(map(int, list(str(combined))))
    for n in new_recipies:
        s.append(n)
        if target == scoreboard[-len(target):]:
            print(len(s) - len(target))
            exit()

    skip_a = (x + 1 + s[x]) % len(s)
    skip_b = (y + 1 + s[y]) % len(s)

    return skip_a, skip_b


scoreboard = [3, 7]
# scoreboard = convert_to_str(scoreboard)
a = 0
b = 1

target = '110201'
target = [int(x) for x in target]

while True:
    a, b = new_score(scoreboard, a, b)
    # print_score(scoreboard, a, b)

# print_score(scoreboard, a, b)

