import pprint
import re
from itertools import combinations

import networkx as nx
from cinnamon_tools.point import Point
from tqdm import trange

pp = pprint.PrettyPrinter(indent=4)


def process_input():
    file = 'a.txt'
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input():
    data = process_input()
    data = [Point(*map(int, d.split(','))) for d in data]

    return data


def main():
    data = get_input()

    g = nx.Graph()

    for p in data:
        g.add_node(p)

    for x, y in combinations(data, 2):
        if x.distance_to(y) <= 3:
            g.add_edge(x,y)
    print(nx.number_connected_components(g))


if __name__ == '__main__':
    main()
