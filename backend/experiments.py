from bb84 import (
    generate_bits,
    generate_bases,
    encode_bits,
    measure_states,
    sift_key,
    calculate_qber
)

from attack import eve_intercept
from noise import apply_bit_flip_noise

import time
import csv


def run_experiment(
    number_of_bits,
    eve_attack,
    interception_rate,
    noise_rate
):

    start_time = time.time()

    # Alice generates bits and bases
    alice_bits = generate_bits(number_of_bits)
    alice_bases = generate_bases(number_of_bits)

    # Alice encodes the bits
    quantum_states = encode_bits(
        alice_bits,
        alice_bases
    )

    # Eve interception
    quantum_states, intercepted_count = eve_intercept(
        quantum_states,
        eve_attack,
        interception_rate
    )

    # Channel noise
    quantum_states, noise_errors = apply_bit_flip_noise(
        quantum_states,
        noise_rate
    )

    # Bob chooses bases
    bob_bases = generate_bases(number_of_bits)

    # Bob measures
    bob_bits = measure_states(
        quantum_states,
        bob_bases
    )

    # Sift the key
    alice_key, bob_key = sift_key(
        alice_bits,
        alice_bases,
        bob_bits,
        bob_bases
    )

    # Calculate QBER
    qber = calculate_qber(
        alice_key,
        bob_key
    )

    execution_time = time.time() - start_time

    return (
        qber,
        len(alice_key),
        intercepted_count,
        noise_errors,
        execution_time
    )


def main():

    number_of_bits = 1000

    eve_rates = [
        0.0,
        0.25,
        0.50,
        0.75,
        1.0
    ]

    noise_rates = [
        0.0,
        0.01,
        0.05,
        0.10,
        0.20
    ]

    results = []

    print("\n==============================================")
    print("        QBER EXPERIMENTS")
    print("==============================================")

    print(
        "\nQubits used for each experiment:",
        number_of_bits
    )

    print("\nStarting experiments...\n")

    for eve_rate in eve_rates:

        for noise_rate in noise_rates:

            if eve_rate == 0:
                eve_attack = False
            else:
                eve_attack = True

            (
                qber,
                key_length,
                intercepted,
                noise_errors,
                execution_time
            ) = run_experiment(
                number_of_bits,
                eve_attack,
                eve_rate,
                noise_rate
            )

            print("----------------------------------------------")

            print(
                f"Eve Rate    : {eve_rate * 100:.0f}%"
            )

            print(
                f"Noise Rate  : {noise_rate * 100:.0f}%"
            )

            print(
                f"QBER        : {qber * 100:.2f}%"
            )

            print(
                f"Key Length  : {key_length}"
            )

            print(
                f"Eve States  : {intercepted}"
            )

            print(
                f"Noise Errors: {noise_errors}"
            )

            print(
                f"Time        : {execution_time:.4f} seconds"
            )

            # Save result
            results.append([
                number_of_bits,
                eve_rate * 100,
                noise_rate * 100,
                qber * 100,
                key_length,
                intercepted,
                noise_errors,
                execution_time
            ])

    # ------------------------------------------
    # SAVE RESULTS TO CSV
    # ------------------------------------------

    with open(
        "results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Qubits",
            "Eve_Rate_Percent",
            "Noise_Rate_Percent",
            "QBER_Percent",
            "Key_Length",
            "Eve_Intercepted",
            "Noise_Errors",
            "Execution_Time"
        ])

        writer.writerows(results)

    print("\n==============================================")
    print("        EXPERIMENTS COMPLETED")
    print("==============================================")

    print("\nResults saved successfully!")

    print("File created: results.csv")


if __name__ == "__main__":

    main()