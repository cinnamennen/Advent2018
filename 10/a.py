import pprint
import re
from operator import itemgetter

import numpy as np
import matplotlib.pyplot as plt

pp = pprint.PrettyPrinter(indent=4)

file = 'a.txt'
data = [_.strip() for _ in open(file).readlines()]
e10 = [[int(z) for z in re.findall(r'-?\d+', x)] for x in data]

n10 = np.array(e10)

coords = n10[:, :2].copy()
vels = n10[:, 2:].copy()


def row_exists(c):
    return len(set(np.array(sorted(c, key=itemgetter(0)))[:6, 0])) == 1


canvas = np.zeros(coords.max(axis=0) + 2)
canvas[coords[:, 0], coords[:, 1]] += 1

for i in range(1, 20000):
    coords += vels
    if row_exists(coords):
        print(i)
        break
# print(coords)

x = coords[:, :1].copy().flatten()
y = coords[:, 1:].copy().flatten()
coords = [(a, b,) for (a, b,) in coords]

# print(coords)
# print(x, y)
# exit()
for b in range(min(y) - 1, max(y) + 2):
    for a in range(min(x) - 1, max(x) + 2):
        # print(a,b)
        if (a, b,) in coords:
            print('#', end='')
        else:
            print('.', end='')
    print('')
