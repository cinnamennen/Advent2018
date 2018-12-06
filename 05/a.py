from string import ascii_uppercase


def process(polymer: str) -> str:
    built_up = []
    sequences = list(polymer)
    for code in sequences:
        if not built_up:
            built_up.append(code)
            continue

        if code.upper() == built_up[-1].upper() and code != built_up[-1]:
            built_up.pop()
            continue
        built_up.append(code)

    return "".join(built_up)


def main():
    file = 'a.txt'
    incoming = [process(_.strip()) for _ in open(file).readlines()]
    print([len(_) for _ in incoming])


if __name__ == '__main__':
    main()
