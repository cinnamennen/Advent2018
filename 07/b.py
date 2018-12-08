import pprint
import re
from collections import Counter
from functools import reduce, total_ordering
from string import ascii_uppercase

import networkx as nx
import matplotlib.pyplot as plt

pp = pprint.PrettyPrinter(indent=4)

file = 'a.txt'
data = [_.strip() for _ in open(file).readlines()]
data = [re.search(r"Step (.*) must be finished before step (.*) can begin\.", x).groups() for x in data]

node_costs = {
    letter: i + 61 for i, letter in enumerate(ascii_uppercase)
}

completed_nodes = set()
ordered_completed_nodes = []


@total_ordering
class Worker:
    def __init__(self):
        self.time_left = 0
        self.node = None
        self.is_working = False

    def __eq__(self, other):
        return self.time_left == other.time_left

    def __lt__(self, other):
        return self.time_left < other.time_left

    def tick(self, time):
        if not self.is_working:
            return
        # print(f"Ticking for {time} seconds")
        self.time_left -= time
        if self.time_left <= 0:
            # print(f"Done with {self.node}")
            self.is_working = False
            completed_nodes.add(self.node)
            ordered_completed_nodes.append(self.node)
            self.node = None
            self.time_left = 0
            # print(f"Completed: {ordered_completed_nodes}")

    def assign_task(self, node):
        self.node = node
        self.time_left = node_costs[node]
        self.is_working = True

    def is_free(self):
        return not self.is_working

    def __repr__(self):
        if self.is_free():
            return "<Worker: Free>"

        return f"<Worker: Node {self.node} - {self.time_left} seconds remaining>"


workers = [Worker() for i in range(5)]
total_time = 0

G = nx.DiGraph(data)
running = []
while len(G) > 0:
    # print(total_time, workers)
    busy_workers = list(filter(lambda w: not w.is_free(), workers))
    tick_time = min(busy_workers).time_left if len(busy_workers) > 0 else 0

    for worker in workers:
        worker.tick(tick_time)
    total_time += tick_time

    # print(total_time, workers)
    # print(completed_nodes)

    for node in filter(lambda n: n in G, completed_nodes):
        G.remove_node(node)
    # print(G.nodes)
    # noinspection PyCallingNonCallable
    in_progress = list(map(lambda w: w.node, workers))
    # print("in flight is", in_progress)

    available_tasks = sorted([t for t in G if t not in in_progress and G.in_degree(t) == 0])
    # print(total_time, workers)

    # print("I can work on:", available_tasks)

    for worker in filter(lambda w: w.is_free(), workers):
        if len(available_tasks) < 1:
            break
        task = available_tasks.pop(0)
        # print(f"Assigning {task}")
        worker.assign_task(task)

print("".join(ordered_completed_nodes))
print(total_time)
