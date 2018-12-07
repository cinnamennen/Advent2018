import pprint
from collections import Counter

pp = pprint.PrettyPrinter(indent=4)


def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


file = 'a.txt'
safe = 10000
data = [_.strip() for _ in open(file).readlines()]
data = [x.split(', ') for x in data]
data = [(int(a), int(b),) for (a, b) in data]

a_s = [a for (a, b) in data]
b_s = [b for (a, b) in data]
min_a = min(a_s) - (safe // len(data)) - 1
min_b = min(b_s) - (safe // len(data)) - 1
max_a = max(a_s) + (safe // len(data)) + 1
max_b = max(b_s) + (safe // len(data)) + 1

# Normalize
data = [(a - min_a, b - min_b) for (a, b,) in data]
max_a -= min_a
max_b -= min_b
min_a = min_b = 0

grid = [[[] for y in range(max_b + 1)] for x in range(max_a + 1)]

for x in range(len(grid)):
    for y in range(len(grid[x])):
        distances = sum([manhattan_dist(x, y, a, b) for (a, b) in data])
        grid[x][y] = distances

grid = [[elem for elem in x if elem < safe] for x in grid]
grid = [item for sublist in grid for item in sublist]

print(len(grid))
