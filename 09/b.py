import pprint
import re
from collections import deque

pp = pprint.PrettyPrinter(indent=4)

file = 'a.txt'
data = [_.strip() for _ in open(file).readlines()]
data = [re.search(r"(\d*) players; last marble is worth (\d*) points", d).groups() for d in data]
data = [list(map(int, d)) for d in data]


def d_print(pos: int, d: list):
    before, at, after = d[:pos], str(d[pos]), d[pos + 1:]
    b = ' ' + "  ".join(map(str, before))
    if b == ' ':
        b = ''
    else:
        b += ' '
    at_ = "(" + at + ") "
    a = "  ".join(map(str, after))
    return b + at_ + a


def nice_print(game, player, position):
    print(player, d_print(position, game))


def next_player(players, current):
    return pad_index((current + 1), players)


def pad_index(index, length):
    index_length = index % length
    # print(f"Padded {index} to {index_length}")
    return index_length


def play_game(players, end):
    game = deque([0])
    scores = {p + 1: 0 for p in range(players)}

    position = 1
    player = 1
    for i in range(1, end + 1):
        player = next_player(players, player)
        if i % 23 == 0:
            game.rotate(7)
            scores[player + 1] += i + game.pop()
            game.rotate(-1)
        else:
            game.rotate(-1)
            game.append(i)
    return max(scores.values())


data = [play_game(p, e*100) for (p, e) in data]

pp.pprint(data)
