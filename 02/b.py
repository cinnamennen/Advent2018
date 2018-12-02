from itertools import combinations
from collections import Counter

data = [_.strip() for _ in open("a.txt").readlines()]


def subtract(a: str, b: str):
    x = [ord(_) for _ in list(a)]
    y = [ord(_) for _ in list(b)]
    diff = [q - r for (q, r) in zip(x, y)]
    if 0 not in diff:
        return
    counter = Counter(diff)
    del counter[0]

    if len(counter) != 1:
        return

    unique = list(counter)[0]
    position = diff.index(unique)

    del x[position]
    del y[position]

    x = "".join([chr(_) for _ in x])
    y = "".join([chr(_) for _ in y])

    assert (x == y)

    print(x)


for (s, t) in (combinations(data, 2)):
    subtract(s, t)
