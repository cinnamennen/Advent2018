import pprint
import re
from typing import List

from tqdm import trange

pp = pprint.PrettyPrinter(indent=4)


def process_input():
    file = 'a.txt'
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input():
    data = process_input()
    ip = int(data.pop(0).split(' ')[-1])
    data = [d.split(' ') for d in data]
    data = tuple([tuple([int(x) if len(x) !=4 else x for x in d]) for d in data])

    return ip, data


def command(input_registers: List[int], op: str, a: int, b: int, c: int) -> List[int]:
    registers = input_registers
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
    iaddr, instructions = get_input()
    registers = [0 for _ in range(6)]
    # registers[iaddr] = 1
    run(instructions, registers, iaddr)


def run(instructions, registers, iaddr):
    ip = registers[iaddr]
    while 0 <= ip < len(instructions):
        registers[iaddr] = ip
        instruction = instructions[ip]
        registers = command(registers, *instruction)
        ip = registers[iaddr]
        ip += 1
        # if registers[5] > 40000:
        #     break
        print(registers)
    print(registers[0])


if __name__ == '__main__':
    main()
