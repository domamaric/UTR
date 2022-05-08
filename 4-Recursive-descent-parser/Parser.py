from sys import stdin


def produkcija_s():
    global INDEX
    print("S", end="")

    try:
        if INPUT_DATA[INDEX] == 'a':
            INDEX += 1
            return produkcija_a() and produkcija_b()
        elif INPUT_DATA[INDEX] == 'b':
            INDEX += 1
            return produkcija_b() and produkcija_a()
    except IndexError:
        return False
    return True


def produkcija_a():
    global INDEX
    print("A", end="")

    try:
        if INPUT_DATA[INDEX] == 'b':
            INDEX += 1
            return produkcija_c()
        elif INPUT_DATA[INDEX] == 'a':
            INDEX += 1
            return True
    except IndexError:
        return False
    return False


def produkcija_b():
    global INDEX
    print("B", end="")

    try:
        if INPUT_DATA[INDEX] == 'c':
            INDEX += 1
            if INPUT_DATA[INDEX] == 'c':
                INDEX += 1
                if produkcija_s():
                    if INPUT_DATA[INDEX] == 'b':
                        INDEX += 1
                        if INPUT_DATA[INDEX] == 'c':
                            INDEX += 1
                            return True
            return False
    except IndexError:
        return True
    return True


def produkcija_c():
    print("C", end="")
    return produkcija_a() and produkcija_a()


if __name__ == '__main__':
    INPUT_DATA = stdin.readline().strip()
    INDEX = 0
    accept = "\nDA" if produkcija_s() and INDEX == len(INPUT_DATA) else "\nNE"
    print(accept)
