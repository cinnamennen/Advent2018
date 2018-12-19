import pprint

pp = pprint.PrettyPrinter(indent=4)


def process_input():
    file = 'a.txt'
    data = [_.strip() for _ in open(file).readlines()]
    return data


def get_input():
    data = process_input()
    ip = int(data.pop(0).split(' ')[-1])
    data = [d.split(' ') for d in data]
    data = tuple([tuple([int(x) if len(x) != 4 else x for x in d]) for d in data])

    return ip, data


def parse(op: str, a: int, b: int, c: int) -> str:
    if op == 'noop':
        print("Hmm, you shouldn't have done that")
    elif op == 'addr':
        """
        (add register)
        stores into register C the result of adding register A and register B.
        """
        return f"registers[{c}] = registers[{a}] + registers[{b}]"
    elif op == 'addi':
        """
        (add immediate) 
        stores into register C the result of adding register A and value B.
        """
        return f"registers[{c}] = registers[{a}] + {b}"
    elif op == 'mulr':
        """
        (multiply register) 
        stores into register C the result of multiplying register A and register B.
        """
        return f"registers[{c}] = registers[{a}] * registers[{b}]"
    elif op == 'muli':
        """
        (multiply immediate) 
        stores into register C the result of multiplying register A and value B.
        """
        return f"registers[{c}] = registers[{a}] * {b}"
    elif op == 'banr':
        """
        (bitwise AND register) 
        stores into register C the result of the bitwise AND of register A and register B.
        """
        return f"registers[{c}] = registers[{a}] & registers[{b}]"
    elif op == 'bani':
        """
        (bitwise AND immediate) 
        stores into register C the result of the bitwise AND of register A and value B.
        """
        return f"registers[{c}] = registers[{a}] & {b}"
    elif op == 'borr':
        """
        (bitwise OR register) 
        stores into register C the result of the bitwise OR of register A and register B.
        """
        return f"registers[{c}] = registers[{a}] | registers[{b}]"
    elif op == 'bori':
        """
        (bitwise OR immediate) 
        stores into register C the result of the bitwise OR of register A and value B.
        """
        return f"registers[{c}] = registers[{a}] | {b}"
    elif op == 'setr':
        """
        (set register) 
        copies the contents of register A into register C. (Input B is ignored.)
        """
        return f"registers[{c}] = registers[{a}]"
    elif op == 'seti':
        """
        (set immediate) stores value A into register C. (Input B is ignored.)
        """
        return f"registers[{c}] = {a}"
    elif op == 'gtir':
        """
        (greater-than immediate/register) 
        sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
        """
        return f"registers[{c}] = {a} > registers[{b}]"
    elif op == 'gtri':
        """
        (greater-than register/immediate) 
        sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
        """
        return f"registers[{c}] = registers[{a}] > {b}"
    elif op == 'gtrr':
        """
        (greater-than register/register) 
        sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
        """
        return f"registers[{c}] = registers[{a}] > registers[{b}]"
    elif op == 'eqir':
        """
        (equal immediate/register) 
        sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
        """
        return f"registers[{c}] = {a} == registers[{b}]"
    elif op == 'eqri':
        """
        (equal register/immediate) 
        sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
        """
        return f"registers[{c}] = registers[{a}] == {b}"
    elif op == 'eqrr':
        """
        (equal register/register) 
        sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
        """
        return f"registers[{c}] = registers[{a}] == registers[{b}]"
    else:
        return f"Could not parse {op}"


def main():
    iaddr, instructions = get_input()
    rs = ['A', 'i', 'B', 'C', 'D', 'E']
    instructions = [parse(*i) for i in instructions]
    for x, v in enumerate(rs):
        instructions = [i.replace(f'registers[{x}]', v) for i in instructions]

    instructions = [
        'i += 16',
        'B = 1',
        'D = 1',
        'C = B * D',
        'C = C == E',
        'i += C',
        'i += 1',
        'A += B',
        'D += 1',
        'C = D > E',
        'i += C',
        'i = 2',
        'B += 1',
        'C = B > E',
        'i += C',
        'i = 1',
        'i *= i',
        'E += 2',
        'E *= E',
        'E *= i',
        'E *= 11',
        'C += 5',
        'C *= i',
        'C += 4',
        'E += C',
        'i += A',
        'i = 0',
        'C = i',
        'C *= i',
        'C += C',
        'C *= C',
        'C *= 14',
        'C *= i',
        'E += C',
        'A = 0',
        'i = 0'
    ]
    pp.pprint(instructions)


if __name__ == '__main__':
    main()
