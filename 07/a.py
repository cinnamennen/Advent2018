import pprint
import re
from collections import Counter
from functools import reduce

pp = pprint.PrettyPrinter(indent=4)

file = 'a.txt'
data = [_.strip() for _ in open(file).readlines()]
data = [re.search(r"Step (.*) must be finished before step (.*) can begin\.", x).groups() for x in data]
data = [(b, a) for (a, b) in data]

steps = sorted(list(set(reduce((lambda x, y: x + y), data))))
# print(steps)

order = []
while steps:
    can_complete = list(steps)
    for step, dependency in data:
        # print(f"{step} depends on {dependency}")
        try:
            can_complete.remove(step)
        except ValueError:
            pass
    # print(f"can work on {can_complete}")
    can_complete = can_complete[0]

    order += sorted(can_complete)
    for done in can_complete:
        steps.remove(done)
    data = [(step, dependency) for (step, dependency) in data if dependency not in order]


print("".join(order))
