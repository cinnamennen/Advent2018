import enum
import operator
import pprint
import re
from copy import copy
from dataclasses import dataclass
from typing import Any

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
             'narrow': '|'}

        return r[self._name_]


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


@dataclass()
class Explorer:
    position: Point
    tool: Tool
    time: timedelta
    target: Point
    depth: int

    def is_valid(self):
        return 0 <= self.position.x < self.target.x + 50 and 0 <= self.position.y < self.target.y + 50 and self.tool.is_viable(
            get_terrain(self.position, self.target, self.depth))

    def __repr__(self):
        return f"{self.position} - {self.tool}"

    def __eq__(self, other):
        return self.position == other.position and self.tool == other.tool

    def move(self, p: Point):
        obj = copy(self)
        obj.position += p
        obj.time += timedelta(minutes=1)
        return obj

    def equip(self, tool: Tool):
        obj = copy(self)
        obj.tool = tool
        obj.time += timedelta(minutes=7)
        return obj

    def sprawl(self):
        options = [self.move(d) for d in directions.values()] + [self.equip(t) for t in Tool]
        return [o for o in options if o.is_valid()]

    def __hash__(self):
        return (hash(repr(self)))


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


def iterate(traverse, visited):
    traverse.sort(key=operator.attrgetter('time'), reverse=True)
    new_places = [e.sprawl() for e in traverse]
    visited |= set(traverse)
    new_places = [n for sublist in new_places for n in sublist if n not in visited]
    traverse = new_places
    return traverse, visited


def main():
    depth, a, b = get_input()
    target = Point(a, b)
    o = Explorer(Point(0, 0), Tool.torch, timedelta(minutes=0), target, depth)
    fake = Explorer(target, Tool.torch, timedelta(minutes=-1), target, depth)
    visited = set()
    traverse = [o]

    traverse, visited = iterate(traverse, visited)
    while fake not in visited or min([d.time.seconds for d in traverse]) >= timedelta(minutes=50).seconds:
        print(min([d.time.seconds//60 for d in traverse]))
        traverse, visited = iterate(traverse, visited)
        # break
    print(traverse)


if __name__ == '__main__':
    main()
