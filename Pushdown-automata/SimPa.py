from collections import deque
from re import match
from sys import stdin

from numpy import array


class Utils:
    """
    Helper class, used for formatted reading from standard input.
    """

    @staticmethod
    def get_input_data(input_str):
        """
        Return formatted array of alphabet symbols.

        `numpy.array` is used for storing input strings, since numpy arrays
        tend to have shorter access time than builtin python lists.
        """
        tmp = array(input_str.split("|"))
        return [array(tmp[i].split(",")) for i in range(len(tmp))]

    @staticmethod
    def get_transitions(input_str):
        """Return formatted `dict` of transition functions (delta)."""
        transitions = dict()
        for x in input_str:
            r = match("^(.+?),(.+?),(.+?)->(.+?),(.+?)$", x)
            current = r.group(1)
            input_symb = r.group(2)
            stack_symb = r.group(3)
            new_state = r.group(4)
            stack_strings = r.group(5)
            transitions[(current, input_symb, stack_symb)] = (
                new_state, stack_strings)
        return transitions


class Stack(deque):
    """
    A stack implementation using `deque` class from `collections` module.

    In stack, a new element is added at one end and an element is removed from
    that end only. `Deque` provides faster append and pop operations as
    compared to list.
    """

    def __init__(self):
        """Initialize a `Stack` object."""
        super().__init__(self)

    def __repr__(self):
        """Return a string as representation of `Stack` class."""
        return "$" if not self else "".join(self)[::-1]

    def push(self, item):
        """Push `item` in the stack."""
        for s in item[::-1]:
            if s != "$":
                self.append(s)
            else:
                break

    def pop_left(self):
        """Return the element from stack in LIFO order."""
        return self.pop()

    def is_empty(self):
        """Return `True` if stack isn't empty."""
        return False if self else True


""" -------- Driver code -------- """
ulaz = [x.strip() for x in stdin.readlines()]

INPUT_STRINGS = array(Utils.get_input_data(ulaz[0]), dtype=object)  # Ulaz
ALL_STATES = ulaz[1].split(",")  # Skup stanja
SYMBOLS = ulaz[2].split(",")  # Skup ulaznih znakova
STACK_SYMBOLS = ulaz[3].split(",")  # Skup znakova stoga
ACCEPTABLE_STATES = ulaz[4].split(",")  # Skup prihvatljivih stanja
STARTING_STATE = ulaz[5]  # Početno stanje
STARTING_STACK = ulaz[6]  # Početni znak stoga
TRANSITIONS = Utils.get_transitions(ulaz[7:])  # Funkcije prijelaza

for string in INPUT_STRINGS:
    stack = Stack()
    fail = False

    Q = STARTING_STATE
    Z = STARTING_STACK
    print("{}#{}|".format(Q, Z), end="")

    for symbol in string:

        while TRANSITIONS.get((Q, "$", Z)) is not None:
            (Q, Z) = TRANSITIONS.get((Q, "$", Z))
            stack.push(Z)
            print("{}#{}|".format(Q, stack), end="")
            if not stack.is_empty():
                Z = stack.pop_left()
            else:
                fail = True
                break

        if not fail and TRANSITIONS.get((Q, symbol, Z)) is not None:
            (Q, Z) = TRANSITIONS.get((Q, symbol, Z))
            stack.push(Z)
            print("{}#{}|".format(Q, stack), end="")
            if not stack.is_empty():
                Z = stack.pop_left()
            else:
                fail = True
        else:
            fail = True

        if fail:
            print("fail|0")
            break
        else:
            pass

    if fail:
        pass
    else:
        while TRANSITIONS.get(
                (Q, "$", Z)) is not None and Q not in ACCEPTABLE_STATES:
            (Q, Z) = TRANSITIONS.get((Q, "$", Z))
            stack.push(Z)
            print("{}#{}|".format(Q, stack), end="")
            if not stack.is_empty():
                Z = stack.pop_left()
            else:
                break
        print(1 if Q in ACCEPTABLE_STATES else 0)
