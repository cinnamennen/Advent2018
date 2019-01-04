import pprint
import re
from operator import itemgetter

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


def main():
    data = get_input()
    strongest, radius = (max(data, key=itemgetter(1)))
    in_range = [n for n in data if n[0].distance_to(strongest) <= radius]
    print(len(in_range))


if __name__ == '__main__':
    main()
