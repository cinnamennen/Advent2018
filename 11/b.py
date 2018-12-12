import pprint
import numpy as np
from tqdm import tqdm

pp = pprint.PrettyPrinter(indent=4)

file = 'x.txt'
data = [_.strip() for _ in open(file).readlines()]

serial_number = 7165
x_offset = y_offset = 3


def fuel_level(x, y):
    rack = (x + 1) + 10
    power = rack * (y + 1)
    power += serial_number
    power *= rack
    return (power // 100 % 10) - 5


grid = np.fromfunction(fuel_level, (300, 300))

best = x = y = size = None

for width in tqdm(range(3, 300)):
    windows = sum(grid[x:x - width + 1 or None, y:y - width + 1 or None] for x in range(width) for y in range(width))
    maximum = int(windows.max())
    location = np.where(windows == maximum)
    a = location[0][0] + 1
    b = location[1][0] + 1
    if best is None or maximum > best:
        best = maximum
        x, y, size = a, b, width

    # print(width, maximum, a, b)

print(f"{x},{y},{size} - {best}")
