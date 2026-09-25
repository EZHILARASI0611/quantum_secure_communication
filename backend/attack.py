import random


def eve_intercept(states, eve_attack=True, interception_rate=1.0):
    """
    Simulate Eve's intercept-and-resend attack.

    states:
        Quantum states sent by Alice

    eve_attack:
        True  -> Eve is active
        False -> Eve is inactive

    interception_rate:
        Percentage of states intercepted by Eve.
        1.0 = 100%
        0.5 = 50%
        0.25 = 25%
    """

    if not eve_attack:
        return states, 0

    intercepted_states = []
    intercepted_count = 0

    for state in states:

        # Decide whether Eve intercepts this state
        if random.random() <= interception_rate:

            intercepted_count += 1

            # Eve randomly chooses a basis
            eve_basis = random.randint(0, 1)

            # Eve measures the state
            measured_bit = measure_state(
                state,
                eve_basis
            )

            # Eve creates a new state
            new_state = create_state(
                measured_bit,
                eve_basis
            )

            intercepted_states.append(new_state)

        else:
            # Eve does not intercept
            intercepted_states.append(state)

    return intercepted_states, intercepted_count


def measure_state(state, basis):
    """
    Eve measures the quantum state.
    """

    # Correct basis measurement

    if basis == 0:

        if state == "|0>":
            return 0

        if state == "|1>":
            return 1

        # Wrong basis gives random result
        return random.randint(0, 1)

    else:

        if state == "|+>":
            return 0

        if state == "|->":
            return 1

        # Wrong basis gives random result
        return random.randint(0, 1)


def create_state(bit, basis):
    """
    Eve prepares a new quantum state
    based on her measurement.
    """

    if basis == 0:

        if bit == 0:
            return "|0>"
        else:
            return "|1>"

    else:

        if bit == 0:
            return "|+>"
        else:
            return "|->"