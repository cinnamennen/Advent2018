import pprint
import re
from operator import itemgetter
from z3 import *

from tqdm import trange
from cinnamon_tools.point import Point

pp = pprint.PrettyPrinter(indent=4)


def process_input():
    file = 'a.txt'
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input():
    data = process_input()
    data = [re.search(r"pos=<(.+)>, r=(.+)", d).groups() for d in data]
    data = [(Point(*map(int, a.split(','))), int(b)) for a, b in data]

    return data


def lenr(l):
    return range(len(l))


def gan(s):
    return map(int, re.findall(r'-?\d+', s))


def main():
    data = get_input()
    nanobots = [((*p,), r) for p, r in data]

    def zabs(x):
        return If(x >= 0, x, -x)

    (x, y, z) = (Int('x'), Int('y'), Int('z'))
    in_ranges = [
        Int('in_range_' + str(i)) for i in lenr(nanobots)
    ]
    range_count = Int('sum')
    o = Optimize()
    for i in lenr(nanobots):
        (nx, ny, nz), nrng = nanobots[i]
        o.add(in_ranges[i] == If(zabs(x - nx) + zabs(y - ny) + zabs(z - nz) <= nrng, 1, 0))
    o.add(range_count == sum(in_ranges))
    dist_from_zero = Int('dist')
    o.add(dist_from_zero == zabs(x) + zabs(y) + zabs(z))
    h1 = o.maximize(range_count)
    h2 = o.minimize(dist_from_zero)
    print(o.check())
    # print o.lower(h1)
    # print o.upper(h1)
    print("b", o.lower(h2), o.upper(h2))
    # print o.model()[x]
    # print o.model()[y]
    # print o.model()[z]


if __name__ == '__main__':
    main()
