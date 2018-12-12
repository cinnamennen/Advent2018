import pprint
import numpy as np

pp = pprint.PrettyPrinter(indent=4)

file = 'x.txt'
data = [_.strip() for _ in open(file).readlines()]

serial_number = 18
x_offset = y_offset = 3


def fuel_level(x, y):
    rack_id = x + 10
    level = rack_id * y
    level += serial_number
    level *= rack_id
    hundreds = int(str(level)[-3])
    hundreds -= 5
    return hundreds


fuel = np.array([[fuel_level(x, y) for y in range(300)] for x in range(300)])

sub = np.array(
    [[[fuel[x:x + size, y:y + size].sum() for y in range(300 - size)] for x in range(300 - size)] for size in range(3)])
# for size in range(301):
#     for x in range(300 - size):
#         for y in range(300 - size):
#             sub[size][x][y] = fuel[x:x + size, y:y + size].sum()
print(sub)
x = y = size = best = -10000000
for s in sub:
    for a in range(len(sub[s])):
        for b in range(len(sub[s][a])):
            if sub[s][a][b] > best:
                best = sub[s][a][b]
                x, y, size = a, b, s
print(f"{x},{y},{size} - {best}")
