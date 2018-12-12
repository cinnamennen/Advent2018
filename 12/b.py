import pprint
from tqdm import tqdm, trange

from collections import Hashable
import functools


class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        # if not isinstance(args, Hashable):
        #     # uncacheable. a list, for instance.
        #     # better to not cache than blow up.
        #     return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__

    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)


pp = pprint.PrettyPrinter(indent=4)

file = 'a.txt'
data = [_.strip() for _ in open(file).readlines()]
start = data.pop(0)[15:]
data.pop(0)
state = start

data = {d[:5]: d[-1] for d in data if d[-1] == '#'}

zero_location = 0


@memoized
def next_state(s: str) -> (str, int):
    m = '.....' + s + '.....'
    new_state = [data.get(m[i: i + 5], '.') for i in range(len(m))]
    new_state = "".join(new_state)
    new_state = new_state.rstrip('.')
    last_state = new_state.lstrip('.')

    removed = len(new_state) - len(last_state)

    return last_state, (removed - 3)

@memoized
def get_value(s, z):
    return sum([index + z for index, value in enumerate(s) if value == '#'])

total_iterations = 50000000000

iterations = 1000

values = [0]
last_value = 0
for _ in (range(int(iterations))):
    state, z_diff = next_state(state)
    zero_location += z_diff
    current_value = get_value(state, zero_location)
    values.append(current_value - last_value)
    last_value = current_value

last_value = sum(values[-100:]) // len(values[-100:])

print(last_value)
print("\n\n\n",sum(values) + (total_iterations-iterations) * last_value)
