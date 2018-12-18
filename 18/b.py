import enum
import pprint
import re
from collections import Counter, deque
from typing import List

from tqdm import trange, tqdm
from cinnamon_tools.point import Point, file_directions

pp = pprint.PrettyPrinter(indent=4)


class Land(enum.Enum):
    open = '.'
    tree = '|'
    lumber = '#'
    bad = '@'

    def __repr__(self):
        return self._value_

    def __str__(self):
        return repr(self)


def safe_get(grid: List[List[Land]], x, y) -> Land:
    if x < 0 or y < 0:
        return Land.bad
    try:
        return unsafe_get(grid, x, y)
    except IndexError:
        return Land.bad


def unsafe_get(grid, x, y):
    return grid[y][x]


def print_grid(grid: List[List[Land]]):
    print()
    for r in grid:
        print("".join(map(str, r)))


def calculate(grid: List[List[Land]], x: int, y: int) -> Land:
    current = safe_get(grid, x, y)
    adjacent = [safe_get(grid, a + x, b + y) for a in range(-1, 2) for b in range(-1, 2)]
    adjacent.remove(current)

    if current == Land.open:
        return Land.tree if adjacent.count(Land.tree) >= 3 else current
    elif current == Land.tree:
        return Land.lumber if adjacent.count(Land.lumber) >= 3 else current
    elif current == Land.lumber:
        return Land.lumber if adjacent.count(Land.lumber) >= 1 and adjacent.count(Land.tree) >= 1 else Land.open
    else:
        return Land.bad


def tick(grid: List[List[Land]]):
    new_grid = [[calculate(grid, x, y) for x in range(len(grid[y]))] for y in range(len(grid))]
    return new_grid


def process_input():
    file = 'a.txt'
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input():
    data = process_input()
    data = [list(map(Land, d)) for d in data]

    return data


def main():
    data = get_input()
    next_data = None
    # print_grid(data)
    seen = deque(maxlen=1000)
    total = 1000000000
    # total = 10
    i = total
    with tqdm(total=i) as t:
        while i > 0:
            next_data = tick(data)
            if seen.count(next_data) > 1:
                # print(f"I can shortcut {total - i}")
                # print("data")
                # print_grid(data)
                # print("seen")
                # for s in seen:
                #     print_grid(s)

                skips = {i: v for i, v in enumerate(seen) if v == next_data}
                keys = list(skips.keys())
                skips = keys[-1] - keys[-2]

                can_skip = i - (i % skips)
                i -= can_skip
                t.update(can_skip)
                seen.clear()

            data = next_data
            seen.append(data)
            i -= 1
            t.update(1)

        # print_grid(data)
    c = Counter([item for sublist in data for item in sublist])

    # print(c)
    print(c[Land.lumber] * c[Land.tree])


if __name__ == '__main__':
    main()
