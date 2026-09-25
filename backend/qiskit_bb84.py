import random

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


# -----------------------------------------
# CREATE RANDOM BITS AND BASES
# -----------------------------------------

def generate_bits(number_of_bits):
    return [
        random.randint(0, 1)
        for _ in range(number_of_bits)
    ]


def generate_bases(number_of_bits):
    return [
        random.randint(0, 1)
        for _ in range(number_of_bits)
    ]


# -----------------------------------------
# CREATE BB84 QUANTUM CIRCUIT
# -----------------------------------------

def create_bb84_circuit(bits, bases):

    number_of_bits = len(bits)

    circuit = QuantumCircuit(
        number_of_bits,
        number_of_bits
    )

    for i in range(number_of_bits):

        # Alice's bit
        if bits[i] == 1:
            circuit.x(i)

        # Alice's basis
        # 0 = Z basis
        # 1 = X basis
        if bases[i] == 1:
            circuit.h(i)

    return circuit


# -----------------------------------------
# BOB MEASUREMENT
# -----------------------------------------

def add_bob_measurements(circuit, bob_bases):

    for i in range(len(bob_bases)):

        # If Bob uses X basis,
        # apply Hadamard before measurement
        if bob_bases[i] == 1:
            circuit.h(i)

        circuit.measure(i, i)

    return circuit


# -----------------------------------------
# SIFT KEY
# -----------------------------------------

def sift_key(
    alice_bits,
    alice_bases,
    bob_results,
    bob_bases
):

    alice_key = []
    bob_key = []

    for i in range(len(alice_bits)):

        if alice_bases[i] == bob_bases[i]:

            alice_key.append(
                alice_bits[i]
            )

            bob_key.append(
                bob_results[i]
            )

    return alice_key, bob_key


# -----------------------------------------
# QBER
# -----------------------------------------

def calculate_qber(alice_key, bob_key):

    if len(alice_key) == 0:
        return 0

    errors = 0

    for alice_bit, bob_bit in zip(
        alice_key,
        bob_key
    ):

        if alice_bit != bob_bit:
            errors += 1

    return errors / len(alice_key)


# -----------------------------------------
# RUN QISKIT BB84
# -----------------------------------------

def run_qiskit_bb84(number_of_bits=20):

    print("\n======================================")
    print("       ACTUAL QISKIT BB84")
    print("======================================")

    # Alice generates random data
    alice_bits = generate_bits(
        number_of_bits
    )

    alice_bases = generate_bases(
        number_of_bits
    )

    # Bob generates random bases
    bob_bases = generate_bases(
        number_of_bits
    )

    # Create quantum circuit
    circuit = create_bb84_circuit(
        alice_bits,
        alice_bases
    )

    # Add Bob's measurements
    circuit = add_bob_measurements(
        circuit,
        bob_bases
    )

    print("\nAlice Bits:")
    print(alice_bits)

    print("\nAlice Bases:")
    print(alice_bases)

    print("\nBob Bases:")
    print(bob_bases)

    # -----------------------------------------
    # RUN QUANTUM SIMULATOR
    # -----------------------------------------

    simulator = AerSimulator()

    result = simulator.run(
        circuit,
        shots=1
    ).result()

    counts = result.get_counts()

    # Get measurement result
    measured_string = list(
        counts.keys()
    )[0]

    # Qiskit returns classical bits
    # in reversed display order
    measured_string = measured_string[::-1]

    bob_results = [
        int(bit)
        for bit in measured_string
    ]

    # -----------------------------------------
    # SIFT KEY
    # -----------------------------------------

    alice_key, bob_key = sift_key(
        alice_bits,
        alice_bases,
        bob_results,
        bob_bases
    )

    # -----------------------------------------
    # QBER
    # -----------------------------------------

    qber = calculate_qber(
        alice_key,
        bob_key
    )

    print("\nBob Measurement:")
    print(bob_results)

    print("\nAlice Sifted Key:")
    print(alice_key)

    print("\nBob Sifted Key:")
    print(bob_key)

    print("\nFinal Key Length:")
    print(len(alice_key))

    print("\nQBER:")
    print(
        f"{qber * 100:.2f}%"
    )

    print("\nQuantum Circuit:")
    print(circuit)

    print("\n======================================")
    print("       QISKIT BB84 COMPLETED")
    print("======================================")


# -----------------------------------------
# START PROGRAM
# -----------------------------------------

if __name__ == "__main__":

    run_qiskit_bb84(
        number_of_bits=10
    )