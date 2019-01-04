import enum
import operator
import pprint
import re
from copy import copy
from dataclasses import dataclass
from typing import Any, List

import numpy as np
from cinnamon_tools.memoized import Memoized
from cinnamon_tools.point import Point, directions
from tqdm import trange
import networkx as nx
from datetime import timedelta

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
             'narrow': '|'
             }

        return r[self._name_]

    def valid_tools(self):
        t = {'rocky': [Tool.torch, Tool.climbing],
             'wet': [Tool.climbing, Tool.neither],
             'narrow': [Tool.torch, Tool.neither]
             }
        return t[self._name_]


class Tool(enum.Enum):
    torch = enum.auto()
    climbing = enum.auto()
    neither = enum.auto()

    def __str__(self):
        return self._name_

    def is_viable(self, terrain: Terrain):
        if terrain == Terrain.rocky:
            return self != Tool.neither
        elif terrain == Terrain.wet:
            return self != Tool.torch
        elif terrain == Terrain.narrow:
            return self != Tool.climbing
        else:
            raise AttributeError


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


def get_risk(target: Point, depth: int) -> List[List[Terrain]]:
    padding = 1 + 10
    t = [[
        get_terrain(Point(x, y), target, depth)
        for x in range(target.x + padding)]
        for y in range(target.y + padding)]
    # t = sum([sum([x.value for x in y]) for y in t])
    return t


def iterate(traverse, visited):
    traverse.sort(key=operator.attrgetter('time'), reverse=False)
    print(traverse[0].time, traverse[-1].time)
    new_places = [e.sprawl() for e in traverse]
    visited |= set(traverse)
    new_places = [n for sublist in new_places for n in sublist if n not in visited]
    traverse = new_places
    return traverse, visited


def main():
    depth, a, b = get_input()
    target = Point(a, b)
    # m = get_risk(target, depth)
    cave = nx.Graph()
    value: Terrain
    for x in range(0, target.x + 1 + 100):
        for y in range(0, target.y + 1 + 100):
            value = get_terrain(Point(x, y), target, depth)
            tools = value.valid_tools()
            cave.add_edge((x, y, tools[0]), (x, y, tools[1]), weight=7)
            movement = [Point(x, y) + d for d in directions.values()]
            movement = [p for p in movement if 0 <= p.x < target.x + 100 and 0 <= p.y < target.y + 100]
            for p in movement:
                new_tools = get_terrain(p, target, depth).valid_tools()
                for tool in set(tools).intersection(set(new_tools)):
                    cave.add_edge((x, y, tool), (*p, tool), weight=1)

    print(nx.dijkstra_path_length(cave, (0, 0, Tool.torch), (*target, Tool.torch)))


if __name__ == '__main__':
    main()
