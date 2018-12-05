import re
from collections import Counter

file = "a.txt"
incoming = [_.strip() for _ in open(file).readlines()]

pattern = re.compile(r"#(\d*) @ (\d*),(\d*): (\d*)x(\d*)")

data = {}
for d in incoming:
    m = {}
    key, m['left'], m['top'], m['width'], m['height'] = re.search(pattern, d).groups()
    for k, v in m.items():
        m[k] = int(v)

    data[key] = m

cloth = [[[] for x in range(1000)] for y in range(1000)]

for key, section in data.items():
    for x in range(section['top'], section['top'] + section['height']):
        for y in range(section['left'], section['left'] + section['width']):
            cloth[x][y].append(key)

to_del = []
for row in cloth:
    for col in row:
        if not col:
            to_del.append((row, col,))

cloth = [[col for col in row if col != []] for row in cloth]

simplified = [item for sublist in [item for sublist in cloth for item in sublist] for item in sublist]
canidates = set(simplified)

prune = set()

# Find overlaps
for row in cloth:
    for col in row:
        if len(col) < 2:
            continue
        prune |= set(col)

print((canidates - prune).pop())
