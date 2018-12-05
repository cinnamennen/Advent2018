import re
from collections import Counter
file = "a.txt"
incoming = [_.strip() for _ in open(file).readlines()]

pattern = re.compile(r"#(\d*) @ (\d*),(\d*): (\d*)x(\d*)")

data = {}
for d in incoming:
    m = {}
    key, m['left'], m['top'], m['width'], m['height'] = re.search(pattern, d).groups()
    for k,v in m.items():
        m[k] = int(v)

    data[key] = m

cloth = [[0 for x in range(1000)] for y in range(1000)]

print(data)
for key, section in data.items():
    for x in range(section['top'], section['top']+section['height']):
        for y in range(section['left'], section['left']+section['width']):
            cloth[x][y] += 1

for row in cloth:
    for col in row:
        print('.' if col==0 else col, end='')
    print("")

counter = Counter([item for sublist in cloth for item in sublist])

del counter[0], counter[1]
print(sum(dict(counter).values()))