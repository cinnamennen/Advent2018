import pprint

pp = pprint.PrettyPrinter(indent=4)

file = 'a.txt'
data = [map(int, _.strip().split()) for _ in open(file).readlines()][0]

current_letter = chr(ord('A') - 1)


def next_letter():
    global current_letter
    current_letter = chr(ord(current_letter) + 1)
    return current_letter


class Node:
    instances = []

    def __init__(self, children_count, meta_count):
        self.__class__.instances.append(self)
        self.key = next_letter()
        self.children_count = children_count
        self.meta_count = meta_count
        self.children = []
        self.meta = []

    def __repr__(self):
        return f"<Node {self.key}>"

    def __call__(self, *args, **kwargs):
        pass


def parse():
    global data
    children, meta, *new_data, = data
    data = new_data

    root = Node(children, meta)
    for c in range(root.children_count):
        root.children.append(parse())

    # print(f'I am {root.key} with remaining {data}')
    root.meta = data[:root.meta_count]
    data = data[root.meta_count:]
    # print(root)

    return root


parse()
print(sum(sum(node.meta) for node in Node.instances))
