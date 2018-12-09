import pprint

pp = pprint.PrettyPrinter(indent=4)

file = 'x.txt'
data = [_.strip() for _ in open(file).readlines()]
