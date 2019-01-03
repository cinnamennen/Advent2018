import pprint
import re

import networkx as nx
from cinnamon_tools.point import Point
from tqdm import trange
import matplotlib.pyplot as plt

pp = pprint.PrettyPrinter(indent=4)

cardinal = {
    'N': Point(0, 1),
    'S': Point(0, -1),
    'E': Point(1, 0),
    'W': Point(-1, 0)
}


def process_input():
    file = 'a.txt'
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_subcomponents(m: str):
    found = []
    built = ''
    while True:
        c, m = m[0], m[1:]
        if c in ['E', 'W', 'N', 'S']:
            built += c
        elif c == '|':
            found.append(built)
            built = ''
        elif c == '(':
            return get_subcomponents(m)
        elif c == ')':
            found.append(built)
            built = ''
            break
        else:
            raise AttributeError
    return found


def build_graph(m: str, grid=None, current_position=Point(0, 0)):
    if grid is None:
        grid = nx.Graph()

    pos = {Point(0, 0)}  # the current positions that we're building on
    stack = []  # a stack keeping track of (starts, ends) for groups
    starts, ends = {Point(0, 0)}, set()  # current possible starting and ending positions

    for c in m:
        if c == '|':
            # an alternate: update possible ending points, and restart the group
            ends.update(pos)
            pos = starts
        elif c in 'NEWS':
            # move in a given direction: add all edges and update our current positions
            direction = cardinal[c]
            for p in pos:
                r = (p, p + direction)
                grid.add_edge(*r)
            pos = {p + direction for p in pos}
        elif c == '(':
            # start of group: add current positions as start of a new group
            stack.append((starts, ends))
            starts, ends = pos, set()
        elif c == ')':
            # end of group: finish current group, add current positions as possible ends
            pos.update(ends)
            starts, ends = stack.pop()
    return grid


def get_input():
    data = [d[1:-1] for d in process_input() if '?' not in d]
    data = [build_graph(d) for d in data]

    return data


def main():
    data = get_input()
    data = [nx.algorithms.shortest_path_length(d, Point(0, 0)) for d in data]
    data = data[0]
    data = [length for length in data.values() if length >= 1000]
    data = len(data)
    # for G in data:
    #     pos = nx.spring_layout(G, iterations=100)
    #     plt.subplot(221)
    #     nx.draw(G, pos, font_size=8)
    #     plt.show()

    print(data)


if __name__ == '__main__':
    main()
