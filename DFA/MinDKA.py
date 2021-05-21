from collections import defaultdict
from functools import lru_cache
from re import match
from sys import stdin

TRANSITIONS = dict()
REACHABLE_TRANSITIONS = dict()
LIST_OF_STATES = list()
SAME_STATES = dict()
RELATIONS = defaultdict(list)
ARRAY = defaultdict(lambda: False)


class Utils:
    """Helper class, used for getting transitions, swapping and formatted
    printing to standard output"""

    @staticmethod
    def swap_list(this, that):
        tmp = []
        for el in that:
            if el in this:
                tmp.append(this[el])
            else:
                tmp.append(el)

        tmp = sorted(list(set(tmp)))
        return tmp

    @staticmethod
    def swap_dict(this):
        tmp = {}

        for transition in REACHABLE_TRANSITIONS:
            key = transition
            val = REACHABLE_TRANSITIONS[key]

            if val in this:
                val = this[val]

            if transition[0] in this:
                key = (this[transition[0]], transition[1])

            tmp[key] = val

        return tmp

    @staticmethod
    @lru_cache(maxsize=None)
    def rmark(tpl):
        ARRAY[tpl] = True

        global RELATIONS
        for relation in RELATIONS[tpl]:
            if not ARRAY[tpl]:
                rmark(relation)

        RELATIONS[tpl] = []

    @staticmethod
    def print_out(new, symbols, fnl_states, fnl_start, fnl_transition_tbl):
        print(",".join(new))
        print(",".join(symbols))
        print(",".join(fnl_states))
        print(fnl_start)

        for s in new:
            for symbol in symbols:
                print("{},{}->{}".format(s, symbol,
                                         fnl_transition_tbl[(s, symbol)]))

    @staticmethod
    def get_transitions(input_str):
        """Return formatted `dict` of transition functions (delta)."""
        for el in input_str:
            r = match("^(.+?),(.+?)->(.+)$", el)
            curr = r.group(1)
            symb = r.group(2)
            nxt = r.group(3)

            global TRANSITIONS
            TRANSITIONS[(curr, symb)] = nxt


def find_reachable_states():
    """Return `list` of reachable states."""
    reachable = []
    tmp = [START_STATE]

    for el in tmp:
        if el not in reachable:
            reachable.append(el)

            for symbol in SYMBOLS:
                tmp.append(TRANSITIONS[(el, symbol)])

    reachable.sort()
    return reachable


def find_reachable_transitions():
    """Return `dict` of reachable transitions."""
    result = dict()
    stat = list()

    for stat in TRANSITIONS:
        if stat[0] in REACHABLE_STATES:
            result[stat] = TRANSITIONS[stat]

    return result


def minimize():
    """Return minimized `dict` of states."""
    result = {}

    global ARRAY
    for a in REACHABLE_STATES:
        for b in REACHABLE_STATES:
            if (a != b) and (
                    a not in ACCEPTABLE_STATES and b in ACCEPTABLE_STATES or a in ACCEPTABLE_STATES and
                    b not in ACCEPTABLE_STATES):
                ARRAY[(a, b)] = True

    for a in REACHABLE_STATES:
        for b in REACHABLE_STATES:
            if a in ACCEPTABLE_STATES and b in ACCEPTABLE_STATES or not (a in ACCEPTABLE_STATES) and not (
                    b in ACCEPTABLE_STATES):
                marked = False

                for c in SYMBOLS:
                    if ARRAY[(TRANSITIONS[a, c], TRANSITIONS[b, c])]:
                        marked = True

                if marked:
                    Utils.rmark((a, b))
                else:
                    for c in SYMBOLS:
                        if TRANSITIONS[(a, c)] != TRANSITIONS[(b, c)]:
                            # global relations
                            RELATIONS[(TRANSITIONS[(a, c)],
                                       TRANSITIONS[(b, c)])].append((a, b))

    same = []
    for a in REACHABLE_STATES:
        for b in REACHABLE_STATES:
            if a != b and not ARRAY[(a, b)]:
                found = False

                for item in same:
                    if (a in item) or (b in item):
                        item.append(a)
                        item.append(b)
                        found = True

                if not found:
                    same.append([a, b])

    for same in [sorted(list(set(item))) for item in same]:
        for item in same:
            result[item] = same[0]

    return result


""" -------- Driver code -------- """
data = [line.strip() for line in stdin.readlines()]

ALL_STATES = data[0].split(',')  # 1. redak: skup stanja
SYMBOLS = data[1].split(',')  # 2. redak: skup simbola
SYMBOLS.sort()
ACCEPTABLE_STATES = data[2].split(',')  # 3. redak: skup prihvatljivih stanja
START_STATE = data[3]  # 4. redak: početno stanje
Utils.get_transitions(data[4:])  # 5.+ redak: funkcije prijelaza
REACHABLE_STATES = find_reachable_states()

for state in ACCEPTABLE_STATES:
    if state in REACHABLE_STATES:
        LIST_OF_STATES.append(state)

LIST_OF_STATES.sort()
REACHABLE_TRANSITIONS = find_reachable_transitions()
SAME_STATES = minimize()

new_states = Utils.swap_list(SAME_STATES, REACHABLE_STATES)
final_start = Utils.swap_list(SAME_STATES, [START_STATE])[0]
final_states = Utils.swap_list(SAME_STATES, LIST_OF_STATES)
final_transition_tbl = Utils.swap_dict(SAME_STATES)

Utils.print_out(new_states, SYMBOLS, final_states,
                final_start, final_transition_tbl)
