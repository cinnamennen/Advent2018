import copy
import enum
import pprint
import re
from collections import Counter
from typing import List, Tuple

from tqdm import trange
from cinnamon_tools.point import Point, file_directions

pp = pprint.PrettyPrinter(indent=4)


class Cell(enum.Enum):
    clay = '#'
    sand = ' '
    spring = '+'
    flow = '|'
    water = '~'
    edge = '.'
    flowing = '@'
    to_flow = '?'

    def __repr__(self):
        return self._value_

    def __str__(self):
        return repr(self)


def process_input():
    file = 'a.txt'
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input():
    data = process_input()
    new_data = []
    for d in data:
        s = d.split(', ')
        f = int(s[0].split('=')[1])
        l = list(map(int, s[1].split('=')[1].split('..')))
        if d[0] == 'x':
            for y in range(l[0], l[1] + 1):
                new_data.append(Point(f, y))
        elif d[0] == 'y':
            for x in range(l[0], l[1] + 1):
                new_data.append(Point(x, f))

        else:
            print(f"unknown")
    new_data.append(Point(500, 0))
    new_data.append(Point(500, 1))
    mins = Point(*map(min, zip(*new_data))) - Point(1, 0)

    data = [d - mins for d in new_data]
    maxs = list(map(max, zip(*data)))

    grid = [[Cell.sand for col in range(maxs[0] + 2)] for row in range(maxs[1] + 1)]
    for p in data:
        grid[p.y][p.x] = Cell.clay
    sp = Point(500, 0) - mins
    grid[sp.y][sp.x] = Cell.spring
    sp = Point(500, 1) - mins
    grid[sp.y][sp.x] = Cell.flow
    return grid, [sp]


def safe_get(grid: List[List[Cell]], x, y):
    return grid[y][x] if 0 <= y < len(grid) and 0 <= x < len(grid[y]) else None


def print_grid(grid: List[List[Cell]], flowing: List[Point] = None):
    if not flowing:
        flowing = []
    for x, y in flowing:
        grid[y][x] = Cell.flowing

    print()
    for r in grid:
        print("".join(map(str, r)))
    for x, y in flowing:
        grid[y][x] = Cell.flow


def is_bounded(grid: List[List[Cell]], x: int, y: int):
    row = [safe_get(grid, x, y) for x in range(len(grid[y]))]
    below = [safe_get(grid, x, y + 1) for x in range(len(grid[y]))]

    # print("bounds check")
    # print_grid([row, below])
    surrounding = [i for i, j in enumerate(row) if j == Cell.clay]
    if len(surrounding) < 2:
        return False
    before = [i for i in surrounding if i < x]
    after = [i for i in surrounding if i > x]
    if len(before) < 1 or len(after) < 1:
        return False
    surrounding = (
        max(before),
        min(after)
    )
    return surrounding if all((below[i] in [Cell.clay, Cell.water] for i in range(surrounding[0] + 1, surrounding[
        1]))) else False


def tick(grid: List[List[Cell]], flowing: List[Point]) -> List[Point]:
    # print(f"ticking {flowing}")
    next_flow = []
    potential = []
    for p in flowing:
        if safe_get(grid, p.x, p.y + 1) == Cell.sand:
            # print(f"{p} is falling")
            grid[p.y + 1][p.x] = Cell.flow
            next_flow.append(Point(p.x, p.y + 1))
            continue
        elif safe_get(grid, p.x, p.y + 1) in [Cell.water, Cell.clay]:
            # print(f"{p} is spreading into ", end='')
            bounds = is_bounded(grid, p.x, p.y)
            if bounds:
                # print("water")
                for x in range(bounds[0] + 1, bounds[1]):
                    grid[p.y][x] = Cell.water
                next_flow.append(p + Point(0, -1))
            else:
                # print("flowing water ", end='')
                left = right = p
                while safe_get(grid, *left) == Cell.flow and safe_get(grid, left.x, left.y+1) in [Cell.water,
                                                                                                  Cell.clay]:
                    left += Point(-1, 0)
                while safe_get(grid, *right) == Cell.flow and safe_get(grid, right.x, right.y+1) in [Cell.water,
                                                                                                   Cell.clay]:
                    right += Point(1, 0)
                if safe_get(grid, *left) == Cell.sand:
                    grid[left.y][left.x] = Cell.to_flow
                    potential.append(left)
                if safe_get(grid, *right) == Cell.sand:
                    grid[right.y][right.x] = Cell.to_flow
                    potential.append(right)
                # print(f"with left {left} and right {right}")

    # if potential:
        # print(f"potential {potential}")
        # print_grid(grid)
    for p in potential:
        grid[p.y][p.x] = Cell.flow
        next_flow.append(p)
    # if potential:
    #     print_grid(grid, next_flow)
    # print(flowing)
    return next_flow


def flatten(grid: List[List[Cell]]) -> str:
    rv = "".join(["".join(map(str, _)) for _ in grid])
    # print(f"flattened to {rv}")
    return rv


def main():
    timeout = 10
    t = timeout
    i = 0
    grid, flowing = get_input()

    while len(flowing) > 0:
        i += 1

        new_flowing = tick(grid, flowing)
        if flowing == new_flowing:
            t -= 1
            continue
        else:
            t = 10
        flowing = new_flowing
    while Cell.clay not in grid[0]:
        grid = grid[1:]
    # print_grid(grid, flowing)
    counts = Counter(flatten(grid))
    print(counts[Cell.water.value])


if __name__ == '__main__':
    main()
