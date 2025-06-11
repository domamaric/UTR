import sys
import re

TRANSITIONS = {}


def parse_input_data(input_line: str) -> list[list[str]]:
    return [sequence.split(",") for sequence in input_line.split("|")]


def parse_transitions(transition_lines: list[str]) -> None:
    for line in transition_lines:
        # Using a more descriptive regex variable name
        match_result = re.match(r"(.*),(.*)->(.*)", line.strip())
        if not match_result:
            print(
                f"Warning: Malformed transition line skipped: {line.strip()}",
                file=sys.stderr,
            )
            continue

        current_state, input_symbol, next_states_str = match_result.groups()

        # If the destination is '#', it means no transition, so we skip it.
        if next_states_str == "#":
            continue

        # Split next states and store them
        next_states = next_states_str.split(",")
        TRANSITIONS[(current_state, input_symbol)] = next_states


def format_output(states_list: list[list[str]]) -> str:
    formatted_sequences = []
    for states_at_step in states_list:
        if not states_at_step:
            formatted_sequences.append("#")
        else:
            # Join states with commas, e.g., "q1,q2"
            formatted_sequences.append(",".join(states_at_step))
    # Join the formatted sequences with '|'
    return "|".join(formatted_sequences)


def get_epsilon_closure(states: set[str]) -> set[str]:
    closure = set(states)  # Start with the initial states
    stack = list(states)  # Use a stack for DFS-like traversal

    while stack:
        current_state = stack.pop()
        # Get states reachable from current_state via epsilon transition
        epsilon_reachable = TRANSITIONS.get((current_state, "$"), [])
        for next_state in epsilon_reachable:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure


def simulate_nfa(input_symbols: list[str], start_state: str) -> list[list[str]]:
    # Initialize current_states with the epsilon closure of the start_state
    current_states = get_epsilon_closure({start_state})
    all_step_results = [sorted(list(current_states))]

    for symbol in input_symbols:
        next_possible_states = set()
        for state in current_states:
            # Get states reachable by consuming the symbol
            direct_transitions = TRANSITIONS.get((state, symbol), [])
            next_possible_states.update(direct_transitions)

        # Apply epsilon closure to all newly reached states
        current_states = get_epsilon_closure(next_possible_states)
        all_step_results.append(sorted(list(current_states)))

    return all_step_results


if __name__ == "__main__":
    # Read all lines from stdin
    file_content = [line.strip() for line in sys.stdin.readlines()]

    # Destructure the input lines for better readability
    # This assumes exactly 6 parts to the input based on your original code.
    try:
        input_strings_raw = file_content[0]
        all_states_raw = file_content[1]
        symbols_raw = file_content[2]
        acceptable_states_raw = file_content[3]
        starting_state = file_content[4]
        transition_lines = file_content[5:]
    except IndexError:
        print(
            "Error: Incomplete input provided. Please check the input format.",
            file=sys.stderr,
        )
        sys.exit(1)  # Exit with an error code

    input_sequences = parse_input_data(input_strings_raw)
    parse_transitions(transition_lines)

    for input_sequence in input_sequences:
        simulation_result = simulate_nfa(input_sequence, starting_state)
        print(format_output(simulation_result))
