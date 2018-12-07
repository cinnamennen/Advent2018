import pprint
from collections import Counter

pp = pprint.PrettyPrinter(indent=4)


def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


file = 'a.txt'
data = [_.strip() for _ in open(file).readlines()]
data = [x.split(', ') for x in data]
data = [(int(a), int(b),) for (a, b) in data]

a_s = [a for (a, b) in data]
b_s = [b for (a, b) in data]
min_a = min(a_s)
min_b = min(b_s)
max_a = max(a_s)
max_b = max(b_s)

# Normalize
data = [(a-min_a, b-min_b) for (a,b,) in data]
max_a -= min_a
max_b -= min_b
min_a = min_b = 0


grid = [[[] for y in range(max_b + 1)] for x in range(max_a + 1)]

for x in range(len(grid)):
    for y in range(len(grid[x])):
        distances = [manhattan_dist(x, y, a, b) for (a, b) in data]
        grid[x][y] = distances

# Simplify
for x in range(len(grid)):
    for y in range(len(grid[x])):
        grid[x][y] = -1 if grid[x][y].count(min(grid[x][y])) > 1 else chr(grid[x][y].index(min(grid[x][y])) + ord('A'))

# print(grid)

discard = set([(min_a, y) for y in range(max_b)]) | \
          set([(max_a, y) for y in range(max_b)]) | \
          set([(x, min_b) for x in range(max_a)]) | \
          set([(x, max_b) for x in range(max_a)])
# print(discard)

discard = set([grid[x][y] for (x, y,) in discard] + [-1])
# print(discard)

grid = [[elem for elem in x if elem not in discard] for x in grid]
# print(grid)

counter = Counter([item for sublist in grid for item in sublist])

print(max(list(counter.values())))
