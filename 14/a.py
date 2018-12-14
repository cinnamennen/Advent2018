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


def new_score(s: List[int], x: int, y: int) -> Tuple[List[int], int, int]:
    combined = s[x] + s[y]
    # print("adding", combined)
    new_recipies = list(map(int, list(str(combined))))
    new_list = s[:] + new_recipies
    skip_a = (x + 1 + new_list[x]) % len(new_list)
    skip_b = (y + 1 + new_list[y]) % len(new_list)

    return new_list, skip_a, skip_b


scoreboard = [3, 7]
a = 0
b = 1

target = 110201


while len(scoreboard) < target:
    scoreboard, a, b = new_score(scoreboard, a, b)
    # print_score(scoreboard, a, b)

for _ in range(10):
    scoreboard, a, b = new_score(scoreboard, a, b)
    # print_score(scoreboard, a, b)

want = scoreboard[target:target+10]
want = "".join(map(str,want))
print(want)
