import re
from datetime import datetime, timedelta, time
import pprint
from collections import defaultdict
import operator

from collections import Counter

pp = pprint.PrettyPrinter(indent=4)

file = "a.txt"
incoming = [_.strip() for _ in open(file).readlines()]

pattern = re.compile(r"\[(.*)\] (.*)")

split = [re.search(pattern, d).groups() for d in incoming]

parsed = [(datetime.strptime(read_time, "%Y-%m-%d %H:%M"), event) for (read_time, event) in split]

data = {read_time: event for (read_time, event,) in parsed}

ordered = [(time, data[time]) for time in sorted(data.keys(), reverse=True)]
# pp.pprint(ordered)

guard = re.compile(r"Guard #(\d*) begins shift")
sleep = re.compile(r"falls asleep")
wake = re.compile(r"wakes up")

sleeptime = defaultdict(list)
most_sleep = defaultdict(timedelta)
active = None

sleep_start = None

while len(ordered) > 0:
    (read_time, event) = ordered.pop()
    guard_change = re.search(guard, event)
    if guard_change:
        active = (guard_change.group(1))
        # print(f"guard is {active}")
        continue

    fall_asleep = re.search(sleep, event)
    if fall_asleep:
        sleep_start = read_time
        # print(f"started sleeping at {time}")
        continue

    wake_up = re.search(wake, event)
    if wake_up:
        # print(f"woke up at {time}")
        # print(f"slept for {time - sleep_start}")
        sleeptime[active] += [(sleep_start.time(), read_time.time())]
        most_sleep[active] += (read_time - sleep_start)
        continue

    print(f"I shouldn't get here with {event} at {read_time}", ordered)

# pp.pprint(most_sleep)
# pp.pprint(sleeptime)

sleepiest = max(most_sleep.items(), key=operator.itemgetter(1))[0]
# print(sleepiest)

sleep_schedule = defaultdict(lambda: 0)
for (start, stop) in sleeptime[sleepiest]:
    for minute in (time(minute=x) for x in range(60)):
        if minute >= start and minute < stop:
            sleep_schedule[minute] += 1
# pp.pprint(sleep_schedule)
tiredest = max(sleep_schedule.items(), key=operator.itemgetter(1))[0].minute

print(int(sleepiest)*tiredest)