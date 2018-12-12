import pprint
import numpy as np

pp = pprint.PrettyPrinter(indent=4)

file = 'x.txt'
data = [_.strip() for _ in open(file).readlines()]

serial_number = 7165
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
sub = np.array([[None for y in range(300 - x_offset)] for x in range(300 - y_offset)])

for x in range(300 - x_offset):
    for y in range(300 - y_offset):
        sub[x][y] = fuel[x:x + x_offset, y:y + y_offset].sum()

index = np.unravel_index(sub.argmax(), sub.shape)
print(f"{index[0]},{index[1]}")
