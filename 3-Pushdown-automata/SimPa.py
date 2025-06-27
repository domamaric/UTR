from collections import deque
from re import match
from sys import stdin


def parse_input_data(input_str):
    """Return formatted array of alphabet symbols."""
    return [part.split(",") for part in input_str.split("|")]


def get_transitions(transition_lines):
    """Return formatted `dict` of transition functions (delta)."""
    transitions = {}

    for line in transition_lines:
        if match_result := match(r"^(.+?),(.+?),(.+?)->(.+?),(.+?)$", line):
            current_state, input_symbol, stack_symbol, new_state, stack_string = (
                match_result.groups()
            )
            transitions[(current_state, input_symbol, stack_symbol)] = (
                new_state,
                stack_string,
            )
    return transitions


class PushdownStack(deque):
    """A stack implementation using `deque` for efficient append and pop operations."""

    def __init__(self):
        """Initialize a `PushdownStack` object."""
        super().__init__()

    def __repr__(self) -> str:
        """Return a string representation of the stack."""
        return "$" if not self else "".join(reversed(self))

    def push(self, item: str) -> None:
        """Push `item` onto the stack."""
        for symbol in reversed(item):
            if symbol != "$":
                self.append(symbol)
            else:
                break

    def pop_left(self) -> str:
        """Pop and return the top element from the stack."""
        return self.pop()

    def is_empty(self) -> bool:
        """Return `True` if the stack is empty."""
        return not bool(self)


def simulate_pushdown_automaton(
    input_strings,
    all_states,
    symbols,
    stack_symbols,
    acceptable_states,
    starting_state,
    starting_stack,
    transitions,
):
    """Simulate the pushdown automaton for each input string."""
    for string in input_strings:
        stack = PushdownStack()
        current_state = starting_state
        current_stack_symbol = starting_stack
        fail = False
        print(f"{current_state}#{current_stack_symbol}|", end="")

        for symbol in string:
            while (
                transitions.get((current_state, "$", current_stack_symbol)) is not None
            ):
                current_state, stack_string = transitions[
                    (current_state, "$", current_stack_symbol)
                ]
                stack.push(stack_string)
                print(f"{current_state}#{stack}|", end="")
                current_stack_symbol = (
                    stack.pop_left() if not stack.is_empty() else None
                )
                if current_stack_symbol is None:
                    fail = True
                    break

            if not fail and (
                transition := transitions.get(
                    (current_state, symbol, current_stack_symbol)
                )
            ):
                current_state, stack_string = transition
                stack.push(stack_string)
                print(f"{current_state}#{stack}|", end="")
                current_stack_symbol = (
                    stack.pop_left() if not stack.is_empty() else None
                )
                if current_stack_symbol is None:
                    fail = True
            else:
                fail = True

            if fail:
                print("fail|0")
                break

        if not fail:
            while (
                transitions.get((current_state, "$", current_stack_symbol))
                and current_state not in acceptable_states
            ):
                current_state, stack_string = transitions[
                    (current_state, "$", current_stack_symbol)
                ]
                stack.push(stack_string)
                print(f"{current_state}#{stack}|", end="")
                current_stack_symbol = (
                    stack.pop_left() if not stack.is_empty() else None
                )
                if current_stack_symbol is None:
                    break
            print(1 if current_state in acceptable_states else 0)


if __name__ == "__main__":
    input_lines = [line.strip() for line in stdin.readlines()]

    INPUT_STRINGS = parse_input_data(input_lines[0])
    ALL_STATES = input_lines[1].split(",")
    SYMBOLS = input_lines[2].split(",")
    STACK_SYMBOLS = input_lines[3].split(",")
    ACCEPTABLE_STATES = input_lines[4].split(",")
    STARTING_STATE = input_lines[5]
    STARTING_STACK = input_lines[6]
    TRANSITIONS = get_transitions(input_lines[7:])

    simulate_pushdown_automaton(
        INPUT_STRINGS,
        ALL_STATES,
        SYMBOLS,
        STACK_SYMBOLS,
        ACCEPTABLE_STATES,
        STARTING_STATE,
        STARTING_STACK,
        TRANSITIONS,
    )
