import pprint
import re
from typing import List

from tqdm import trange, tqdm

pp = pprint.PrettyPrinter(indent=4)


def process_input():
    file = 'a.txt'
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input():
    data = process_input()

    data = [d for d in data if d != '']
    training = []
    instructions = []

    while True:
        try:
            before, op, after = data.pop(0), data.pop(0), data.pop(0)
            if 'Before' in before and 'After' in after:
                training.append((list(map(int, re.findall(r"\d+", before))),
                                 list(map(int, re.findall(r"\d+", op))),
                                 list(map(int, re.findall(r"\d+", after)))))
            else:
                instructions += [before, op, after]
                break
        except IndexError:
            break
    instructions += data

    return training, [list(map(int, re.findall(r"\d+", i))) for i in instructions]


def command(input_registers: List[int], op: str, a: int, b: int, c: int) -> List[int]:
    registers = input_registers.copy()
    if op == 'noop':
        print("Hmm, you shouldn't have done that")
    elif op == 'addr':
        """
        (add register)
        stores into register C the result of adding register A and register B.
        """
        registers[c] = registers[a] + registers[b]
    elif op == 'addi':
        """
        (add immediate) 
        stores into register C the result of adding register A and value B.
        """
        registers[c] = registers[a] + b
    elif op == 'mulr':
        """
        (multiply register) 
        stores into register C the result of multiplying register A and register B.
        """
        registers[c] = registers[a] * registers[b]
    elif op == 'muli':
        """
        (multiply immediate) 
        stores into register C the result of multiplying register A and value B.
        """
        registers[c] = registers[a] * b
    elif op == 'banr':
        """
        (bitwise AND register) 
        stores into register C the result of the bitwise AND of register A and register B.
        """
        registers[c] = registers[a] & registers[b]
    elif op == 'bani':
        """
        (bitwise AND immediate) 
        stores into register C the result of the bitwise AND of register A and value B.
        """
        registers[c] = registers[a] & b
    elif op == 'borr':
        """
        (bitwise OR register) 
        stores into register C the result of the bitwise OR of register A and register B.
        """
        registers[c] = registers[a] | registers[b]
    elif op == 'bori':
        """
        (bitwise OR immediate) 
        stores into register C the result of the bitwise OR of register A and value B.
        """
        registers[c] = registers[a] | b
    elif op == 'setr':
        """
        (set register) 
        copies the contents of register A into register C. (Input B is ignored.)
        """
        registers[c] = registers[a]
    elif op == 'seti':
        """
        (set immediate) stores value A into register C. (Input B is ignored.)
        """
        registers[c] = a
    elif op == 'gtir':
        """
        (greater-than immediate/register) 
        sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
        """
        registers[c] = 1 if a > registers[b] else 0
    elif op == 'gtri':
        """
        (greater-than register/immediate) 
        sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
        """
        registers[c] = 1 if registers[a] > b else 0
    elif op == 'gtrr':
        """
        (greater-than register/register) 
        sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
        """
        registers[c] = 1 if registers[a] > registers[b] else 0
    elif op == 'eqir':
        """
        (equal immediate/register) 
        sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        """
        registers[c] = 1 if a == registers[b] else 0
    elif op == 'eqri':
        """
        (equal register/immediate) 
        sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        """
        registers[c] = 1 if registers[a] == b else 0
    elif op == 'eqrr':
        """
        (equal register/register) 
        sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
        """
        registers[c] = 1 if registers[a] == registers[b] else 0
    else:
        print(f"Could not parse {op}")

    return registers


def main():
    ops = {'addr',
           'addi',
           'mulr',
           'muli',
           'banr',
           'bani',
           'borr',
           'bori',
           'setr',
           'seti',
           'gtir',
           'gtri',
           'gtrr',
           'eqir',
           'eqri',
           'eqrr',
           }
    possibilities = {k: ops.copy() for k in range(16)}
    training, instructions = get_input()

    for before, instruction, after in training:
        o, a, b, c = instruction
        to_remove = set()
        for possible_op in possibilities[o]:
            theoretical_result = command(before, possible_op, a, b, c)
            if theoretical_result != after:
                to_remove.add(possible_op)
        possibilities[o] -= to_remove
    new_possibilities = {k: list(v)[0] for k, v in possibilities.items() if len(v) == 1}
    possibilities.update(new_possibilities)
    while len([k for k, v in possibilities.items() if isinstance(v, str)]) != 16:
        known = {v for v in possibilities.values() if isinstance(v, str)}
        for k in possibilities.keys():
            if isinstance(possibilities[k], str):
                continue
            possibilities[k] -= known
        new_possibilities = {k: list(v)[0] for k, v in possibilities.items() if len(v) == 1}
        possibilities.update(new_possibilities)
    # pp.pprint(instructions)

    registers = [0, 0, 0, 0]
    for op, a, b, c in tqdm(instructions):
        registers = command(registers, possibilities[op], a, b, c)
    print(registers[0])


if __name__ == '__main__':
    main()
