import enum
import operator
import pprint
import re
from dataclasses import dataclass, field, InitVar, asdict
from functools import total_ordering
from typing import List, Any, ClassVar

from tqdm import trange

pp = pprint.PrettyPrinter(indent=4)


def process_input():
    file = 'a.txt'
    data = [_.strip() for _ in open(file).readlines()]
    return data


def parse(data: list, team, boost=0):
    v = [re.match(
        r"(?P<units>\d+) units each with (?P<hp>\d+).*? hit points (?P<properties>\(.*\))?.*? (?P<damage>\d+) ("
        r"?P<attack>\w+) damage at initiative (?P<initiative>\d+)",
        d).groupdict() for d in data]
    for d in v:
        p = d.pop('properties')
        for k, i in d.items():
            d[k] = int(i) if k != 'attack' else i
        d['weak'] = []
        d['immune'] = []
        if p:
            p = p[1:-1].split('; ')
        else:
            p = []
        for x in p:
            if 'weak' in x:
                d['weak'] = x.replace('weak to ', '').split(', ')
            if 'immune' in x:
                d['immune'] = x.replace('immune to ', '').split(', ')

    # print('v', v)
    v = [Group(**d, team=team, boost=boost) for d in v]
    return v


def get_input(boost=0):
    data = process_input()
    Group.next_immune_id = 1
    Group.next_infection_id = 1
    immune, infection = data[:data.index('')][1:], data[data.index('') + 1:][1:]
    immune, infection = parse(immune, Team.immune, boost), parse(infection, Team.infect, boost)

    return immune + infection


@total_ordering
class Team(enum.Enum):
    immune = enum.auto()
    infect = enum.auto()

    def __str__(self):
        return self._name_.capitalize()

    def __gt__(self, other):
        return self.value > other.value


@dataclass
class Group:
    initiative: int
    units: int
    damage: int
    hp: int
    weak: List[str]
    immune: List[str]
    attack: str
    team: Team
    id: int = field(init=False)
    boost: InitVar[int] = 0
    target: Any = None
    next_infection_id: ClassVar = 1
    next_immune_id: ClassVar = 1
    targeted: ClassVar = []

    def __post_init__(self, boost):
        id_attr = 'next_infection_id' if self.team == Team.infect else 'next_immune_id'
        self.id = getattr(self.__class__, id_attr)
        setattr(self.__class__, id_attr, getattr(self.__class__, id_attr) + 1)

        if self.team == Team.immune:
            self.damage += boost

    @property
    def effective_power(self) -> int:
        return self.damage * self.units

    def __repr__(self):
        return f"{str(self.team)} {self.id}"

    def set_target(self, units: List[Any]):
        self.target = None
        potential_targets = [u for u in units if
                             u.team != self.team and u != self and u not in self.__class__.targeted]
        # pp.pprint(potential_targets)
        for target in potential_targets:
            dealt = target.damage_dealt(self)
            # print(f"{self} would deal {target} {dealt} damage")
            if dealt < 1:
                continue
            if self.target is None:
                self.target = target
                continue
            if dealt >= self.target.damage_dealt(self):
                if dealt > self.target.damage_dealt(self):
                    self.target = target
                else:
                    if target.effective_power > self.target.effective_power:
                        self.target = target
                    elif target.effective_power < self.target.effective_power:
                        continue
                    else:
                        if target.initiative > self.target.initiative:
                            self.target = target
        self.__class__.targeted.append(self.target)

    def damage_dealt(self, attacker) -> int:
        if attacker.attack in self.immune:
            return 0
        elif attacker.attack in self.weak:
            return attacker.effective_power * 2
        else:
            return attacker.effective_power

    def fight(self):
        if self.units < 1 or self.target is None:
            return False
        to_kill = self.target.units_killed(self)
        # print(f'{str(self)} would attack {str(self.target)} killing { to_kill }')
        self.target.units -= to_kill
        if to_kill < 1:
            return False
        else:
            return True

    def units_killed(self, attacker):
        return min(self.damage_dealt(attacker) // self.hp, self.units)


def run_simulation(units: List[Group]):
    # Target Selection
    units.sort(key=lambda u: (u.team, u.effective_power, -u.initiative), reverse=True)
    # pp.pprint(units)
    Group.targeted = []
    for g in units:
        g.set_target(units)
    # print()

    units.sort(key=lambda u: u.initiative, reverse=True)

    fighting = [g.fight() for g in units]
    if not any(fighting):
        return False
    # print()

    to_remove = [u for u in units if u.units < 1]
    for r in to_remove:
        units.remove(r)
    return True


def reindeer_win(boost: int = 0):
    units = get_input(boost)
    while len([u for u in units if u.team == Team.immune]) > 0 \
        and len([u for u in units if u.team == Team.infect]) > 0:
        fought = run_simulation(units)
        if not fought:
            return False

    rv = {u.team for u in units}
    if len(rv) != 1:
        raise ValueError
    rv = rv.pop()
    if rv == Team.infect:
        return False
    else:
        return sum([u.units for u in units])


def main():
    too_low = 0
    winnable_boost = 1
    while not reindeer_win(winnable_boost):
        too_low, winnable_boost = winnable_boost, winnable_boost * 2

    while winnable_boost - too_low != 1:
        midpoint = too_low + (winnable_boost - too_low) // 2
        # print(midpoint)
        if reindeer_win(midpoint):
            winnable_boost = midpoint
        else:
            too_low = midpoint

    # print(winnable_boost)
    print(reindeer_win(winnable_boost))


if __name__ == '__main__':
    main()
