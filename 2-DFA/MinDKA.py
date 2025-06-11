import sys
import re
from collections import defaultdict

# Module-level constants
TRANSITIONS = {}
ALL_STATES = []
SYMBOLS = []
ACCEPTABLE_STATES = []
START_STATE = ""


def parse_dfa_input(input_lines: list[str]) -> None:
    global ALL_STATES, SYMBOLS, ACCEPTABLE_STATES, START_STATE, TRANSITIONS

    try:
        ALL_STATES = input_lines[0].strip().split(",")
        SYMBOLS = sorted(
            input_lines[1].strip().split(",")
        )  # Sort symbols for consistent output
        ACCEPTABLE_STATES = input_lines[2].strip().split(",")
        START_STATE = input_lines[3].strip()

        # Parse transitions
        for line in input_lines[4:]:
            match_result = re.match(r"^(.+?),(.+?)->(.+)$", line.strip())
            if not match_result:
                print(
                    f"Warning: Malformed transition line skipped: {line.strip()}",
                    file=sys.stderr,
                )
                continue
            current_state, symbol, next_state = match_result.groups()
            TRANSITIONS[(current_state, symbol)] = next_state
    except IndexError as e:
        print(
            f"Error: Incomplete or malformed input. Missing lines: {e}", file=sys.stderr
        )
        sys.exit(1)


def find_reachable_states() -> set[str]:
    reachable = set()
    queue = [START_STATE]  # Use a list as a queue for BFS

    while queue:
        current_state = queue.pop(0)  # Pop from the beginning for BFS
        if current_state not in reachable:
            reachable.add(current_state)
            for symbol in SYMBOLS:
                # Get the next state. If a transition is missing, it's an error
                # in DFA definition (or implies a trap state if not defined).
                next_state = TRANSITIONS.get((current_state, symbol))
                if next_state:
                    queue.append(next_state)
    return reachable


def find_distinguishable_pairs(
    reachable_states: set[str],
) -> dict[tuple[str, str], bool]:
    # Initialize the distinguishability table (M in common algorithms)
    # Using a dictionary for sparse storage, False means not distinguishable yet.
    distinguishable_table = defaultdict(bool)
    # Store relations for marking later
    relations_to_mark = defaultdict(list)  # { (q_i, q_j): [ (q_k, q_l), ... ] }
    sorted_reachable_states = sorted(list(reachable_states))

    # Phase 1: Mark (p, q) if p is accepting and q is non-accepting
    for i, state1 in enumerate(sorted_reachable_states):
        for j in range(
            i + 1, len(sorted_reachable_states)
        ):  # Only consider unique pairs
            state2 = sorted_reachable_states[j]

            pair = (state1, state2)
            if state1 > state2:  # Ensure consistent ordering for the key
                pair = (state2, state1)

            is_state1_accepting = state1 in ACCEPTABLE_STATES
            is_state2_accepting = state2 in ACCEPTABLE_STATES

            if is_state1_accepting != is_state2_accepting:
                distinguishable_table[pair] = True

    # Phase 2: Iteratively mark pairs
    # Keep iterating until no new pairs are marked in an iteration
    something_marked_in_this_pass = True
    while something_marked_in_this_pass:
        something_marked_in_this_pass = False
        for i, state1 in enumerate(sorted_reachable_states):
            for j in range(i + 1, len(sorted_reachable_states)):
                state2 = sorted_reachable_states[j]

                pair = (state1, state2)
                if state1 > state2:
                    pair = (state2, state1)

                if distinguishable_table[pair]:  # Already marked, skip
                    continue

                for symbol in SYMBOLS:
                    next_state1 = TRANSITIONS.get((state1, symbol))
                    next_state2 = TRANSITIONS.get((state2, symbol))

                    # If transitions lead to undefined states, they are distinguishable
                    # This handles cases where original DFA might not be total.
                    if not next_state1 or not next_state2:
                        # If one is defined and other is not, they are distinguishable
                        if next_state1 != next_state2:
                            if not distinguishable_table[pair]:
                                distinguishable_table[pair] = True
                                something_marked_in_this_pass = True
                                break  # Mark this pair and move to next (state1, state2) pair
                        continue  # Both undefined, no immediate distinction

                    # Sort the tuple to ensure canonical key for the table
                    next_pair = (next_state1, next_state2)
                    if next_state1 > next_state2:
                        next_pair = (next_state2, next_state1)

                    if distinguishable_table[next_pair]:
                        if not distinguishable_table[pair]:
                            distinguishable_table[pair] = True
                            something_marked_in_this_pass = True
                            break  # Marked, move to next (state1, state2) pair
                    else:
                        # If (next_state1, next_state2) is not yet marked,
                        # then (state1, state2) is indistinguishable FOR NOW.
                        relations_to_mark[next_pair].append(pair)

    return distinguishable_table


def get_equivalent_states(
    reachable_states: set[str], distinguishable_table: dict[tuple[str, str], bool]
) -> dict[str, str]:
    # Initialize each state as its own representative
    representative_map = {state: state for state in reachable_states}
    # Find and merge equivalent states
    # Iterate over all pairs of reachable states
    sorted_reachable_states = sorted(list(reachable_states))
    for i, state1 in enumerate(sorted_reachable_states):
        for j in range(i + 1, len(sorted_reachable_states)):
            state2 = sorted_reachable_states[j]

            pair = (state1, state2)
            if state1 > state2:
                pair = (state2, state1)

            # If the pair is not distinguishable, they are equivalent
            if not distinguishable_table[pair]:
                # Find the current representatives of state1 and state2
                rep1 = find_representative(state1, representative_map)
                rep2 = find_representative(state2, representative_map)

                if rep1 != rep2:
                    if rep1 < rep2:
                        representative_map[rep2] = rep1
                    else:
                        representative_map[rep1] = rep2

    # Path compression: Ensure all states directly point to their ultimate representative
    for state in reachable_states:
        representative_map[state] = find_representative(state, representative_map)

    return representative_map


def find_representative(state: str, representative_map: dict[str, str]) -> str:
    if representative_map[state] == state:
        return state
    representative_map[state] = find_representative(
        representative_map[state], representative_map
    )
    return representative_map[state]


def construct_minimized_dfa(
    reachable_states: set[str], equivalent_states_map: dict[str, str]
) -> tuple[list[str], list[str], list[str], str, dict[tuple[str, str], str]]:
    new_states_set = set()
    for state in reachable_states:
        new_states_set.add(equivalent_states_map[state])
    new_states = sorted(list(new_states_set))

    final_start_state = equivalent_states_map[START_STATE]

    final_acceptable_states_set = set()
    for state in ACCEPTABLE_STATES:
        if state in reachable_states:  # Only consider reachable accepting states
            final_acceptable_states_set.add(equivalent_states_map[state])
    final_acceptable_states = sorted(list(final_acceptable_states_set))

    final_transition_table = {}
    for current_rep_state in new_states:
        original_state_in_class = (
            current_rep_state  # This works because representatives are original states
        )

        # Since our `equivalent_states_map` uses the lexicographically smallest state as
        # the representative, then this `original_state_in_class` is valid.
        for symbol in SYMBOLS:
            # Find the transition from original_state_in_class
            next_original_state = TRANSITIONS.get((original_state_in_class, symbol))
            if next_original_state:
                # The next state in the minimized DFA is the representative of next_original_state
                final_transition_table[(current_rep_state, symbol)] = (
                    equivalent_states_map[next_original_state]
                )
            else:
                pass  # Depending on problem spec, might need to map to a trap state

    return (
        new_states,
        SYMBOLS,
        final_acceptable_states,
        final_start_state,
        final_transition_table,
    )


def print_minimized_dfa(
    new_states: list[str],
    symbols: list[str],
    final_acceptable_states: list[str],
    final_start_state: str,
    final_transition_table: dict[tuple[str, str], str],
) -> None:
    """
    Prints the minimized DFA definition to standard output.
    """
    print(",".join(new_states))
    print(",".join(symbols))
    print(",".join(final_acceptable_states))
    print(final_start_state)

    # Sort transitions for consistent output
    sorted_transitions = sorted(final_transition_table.items())

    for (state, symbol), next_state in sorted_transitions:
        print(f"{state},{symbol}->{next_state}")


if __name__ == "__main__":
    # Read all lines from stdin
    input_data = [line.strip() for line in sys.stdin.readlines()]

    parse_dfa_input(input_data)
    reachable_states_set = find_reachable_states()

    # Filter acceptable states to only include reachable ones, and sort them
    # This is handled within construct_minimized_dfa now for consistency.
    # reachable_acceptable_states = sorted([s for s in ACCEPTABLE_STATES if s in reachable_states_set])
    distinguishable_table = find_distinguishable_pairs(reachable_states_set)
    equivalent_states_map = get_equivalent_states(
        reachable_states_set, distinguishable_table
    )

    (
        new_states,
        final_symbols,
        final_acceptable_states,
        final_start_state,
        final_transition_table,
    ) = construct_minimized_dfa(reachable_states_set, equivalent_states_map)

    print_minimized_dfa(
        new_states,
        final_symbols,
        final_acceptable_states,
        final_start_state,
        final_transition_table,
    )
