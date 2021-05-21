from re import match
from sys import stdin

TRANSITIONS = dict()


class Utils:
    """
    Helper class, used for formatted reading and printing to standard input.
    """

    @staticmethod
    def get_input_data(input_str):
        """Return formatted array of alphabet symbols."""
        tmp = input_str.split("|")
        return [tmp[i].split(",") for i in range(len(tmp))]

    @staticmethod
    def get_transitions(input_str):
        """Return formatted `dict` of transition functions (delta)."""
        for line in input_str:
            r = match(r'(.*),(.*)->(.*)', line)
            if r.group(3) == '#':
                continue

            trenutno_stanje = r.group(1)
            ulazni_simbol = r.group(2)
            sljedece_stanje = r.group(3).split(",")
            TRANSITIONS[(trenutno_stanje, ulazni_simbol)] = sljedece_stanje
        return

    @staticmethod
    def format_print(input_str):
        """Return formatted string to be printed on `stdout`."""
        result = str()
        length = len(input_str)

        for i in range(length):
            temp = str()
            temp_len = len(input_str[i])

            if temp_len == 0:
                temp = "#"
            else:
                for j in range(temp_len):
                    temp += str(input_str[i][j])
                    if j < temp_len - 1:
                        temp += ","

            result += temp
            if i < length - 1:
                result += "|"

        return result


def sim_automata(symbol, starting):
    result = list()
    current_states = list()

    for i in range(-1, len(symbol)):
        next_states = []
        temp = []

        if i == -1:
            next_states = []
            temp = [starting]
        else:
            for trenutno in current_states:
                transition = TRANSITIONS.get((trenutno, symbol[i]), [])

                for e in transition:
                    if e not in next_states:
                        next_states.append(e)
                        epsilons = TRANSITIONS.get((e, "$"), [])

                        for epsilon in epsilons:
                            temp.append(epsilon)

        while len(temp):
            tmp = temp.pop()

            if tmp not in next_states:
                next_states.append(tmp)

            for e in TRANSITIONS.get((tmp, "$"), []):
                if e not in next_states:
                    temp.append(e)

        result.append(sorted(next_states))
        current_states = next_states

    return result


if __name__ == '__main__':
    file = [x.strip() for x in stdin.readlines()]

    INPUT_STRINGS = Utils.get_input_data(file[0])  # 1. redak, ulazni nizovi
    ALL_STATES = file[1].split(",")  # 2. redak, skup stanja
    SYMBOLS = file[2].split(",")  # 3. redak, skup simbola abecede
    ACCEPTABLE_STATES = file[3].split(",")  # 4. redak, skup prihvatljivih stanja
    STARTING_STATE = file[4]  # 5. redak, početno stanje
    Utils.get_transitions(file[5:])  # funkcije prijelaza u automatu

    for string in INPUT_STRINGS:
        to_print = sim_automata(string, STARTING_STATE)
        print(Utils.format_print(to_print))
