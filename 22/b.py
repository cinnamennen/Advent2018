import enum
import pprint
import re
from dataclasses import dataclass

from cinnamon_tools.memoized import Memoized
from cinnamon_tools.point import Point
from tqdm import trange
import networkx as nx

pp = pprint.PrettyPrinter(indent=4)


def process_input():
    file = 'a.txt'
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input():
    data = process_input()
    data = [re.findall(r'\d+', d) for d in data]
    data = [item for sublist in data for item in sublist]
    data = list(map(int, data))

    return data


class Terrain(enum.Enum):
    rocky = 0
    wet = 1
    narrow = 2

    def __str__(self):
        r = {'rocky': '.',
             'wet': '=',
             'narrow': '|'}

        return r[self._name_]


class Tool(enum.Enum):
    pass


@dataclass
class Explorer:
    pass


@Memoized
def get_ero(p: Point, target: Point, depth: int) -> int:
    return (get_geo(p, target, depth) + depth) % 20183


@Memoized
def get_geo(p: Point, target: Point, depth: int) -> int:
    if p.zero_distance() == 0:
        return 0
    elif p == target:
        return 0
    elif p.y == 0:
        return p.x * 16807
    elif p.x == 0:
        return p.y * 48271
    else:
        return get_ero(p + Point(-1, 0), target, depth) * get_ero(p + Point(0, -1), target, depth)


@Memoized
def get_terrain(p: Point, target: Point, depth: int) -> Terrain:
    return Terrain(get_ero(p, target, depth) % 3)


def get_risk(target: Point, depth: int) -> int:
    t = [[get_terrain(Point(x, y), target, depth) for x in range(target.x + 1)] for y in range(target.y + 1)]
    t = sum([sum([x.value for x in y]) for y in t])
    return t


def main():
    depth, a, b = get_input()
    target = Point(a, b)
    print(get_risk(target, depth))


if __name__ == '__main__':
    main()
