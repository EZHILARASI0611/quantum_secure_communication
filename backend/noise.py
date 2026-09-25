import random


def apply_bit_flip_noise(states, noise_rate):

    noisy_states = []
    errors = 0

    for state in states:

        if random.random() < noise_rate:

            errors += 1

            if state == "|0>":
                state = "|1>"

            elif state == "|1>":
                state = "|0>"

            elif state == "|+>":
                state = "|->"

            elif state == "|->":
                state = "|+>"

        noisy_states.append(state)

    return noisy_states, errors