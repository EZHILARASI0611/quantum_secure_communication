import random
from attack import eve_intercept
from noise import apply_bit_flip_noise


# Generate random bits for Alice
def generate_bits(number_of_bits):
    return [random.randint(0, 1) for _ in range(number_of_bits)]


# Generate random bases for Alice/Bob
# 0 = Rectilinear basis
# 1 = Diagonal basis
def generate_bases(number_of_bits):
    return [random.randint(0, 1) for _ in range(number_of_bits)]


# Encode Alice's bits into quantum states
def encode_bits(bits, bases):
    states = []

    for bit, basis in zip(bits, bases):

        if basis == 0:
            if bit == 0:
                states.append("|0>")
            else:
                states.append("|1>")

        else:
            if bit == 0:
                states.append("|+>")
            else:
                states.append("|->")

    return states


# Bob measures the quantum states
def measure_states(states, bob_bases):
    measured_bits = []

    for state, basis in zip(states, bob_bases):

        if basis == 0:

            if state == "|0>":
                measured_bits.append(0)

            elif state == "|1>":
                measured_bits.append(1)

            else:
                # Wrong basis gives random result
                measured_bits.append(random.randint(0, 1))

        else:

            if state == "|+>":
                measured_bits.append(0)

            elif state == "|->":
                measured_bits.append(1)

            else:
                # Wrong basis gives random result
                measured_bits.append(random.randint(0, 1))

    return measured_bits


# Keep only positions where Alice and Bob used the same basis
def sift_key(alice_bits, alice_bases, bob_bits, bob_bases):

    alice_key = []
    bob_key = []

    for i in range(len(alice_bits)):

        if alice_bases[i] == bob_bases[i]:

            alice_key.append(alice_bits[i])
            bob_key.append(bob_bits[i])

    return alice_key, bob_key


# Calculate Quantum Bit Error Rate
def calculate_qber(alice_key, bob_key):

    if len(alice_key) == 0:
        return 0

    errors = 0

    for alice_bit, bob_bit in zip(alice_key, bob_key):

        if alice_bit != bob_bit:
            errors += 1

    qber = errors / len(alice_key)

    return qber


# Main BB84 process
def run_bb84(
    number_of_bits=20,
    eve_attack=False,
    interception_rate=1.0,
    noise_rate=0.0
):

    print("\n======================================")
    print("   QUANTUM-SAFE SECURE COMMUNICATION")
    print("======================================")

    # -----------------------------
    # STEP 1: Alice generates bits
    # -----------------------------

    alice_bits = generate_bits(number_of_bits)

    alice_bases = generate_bases(number_of_bits)

    # -----------------------------
    # STEP 2: Alice encodes bits
    # -----------------------------

    quantum_states = encode_bits(
        alice_bits,
        alice_bases
    )

    # -----------------------------
    # STEP 3: Eve interception
    # -----------------------------

    quantum_states, intercepted_count = eve_intercept(
        quantum_states,
        eve_attack,
        interception_rate
    )

    # -----------------------------
    # STEP 4: Channel noise
    # -----------------------------

    quantum_states, noise_errors = apply_bit_flip_noise(
        quantum_states,
        noise_rate
    )

    # -----------------------------
    # STEP 5: Bob chooses bases
    # -----------------------------

    bob_bases = generate_bases(number_of_bits)

    # -----------------------------
    # STEP 6: Bob measures states
    # -----------------------------

    bob_bits = measure_states(
        quantum_states,
        bob_bases
    )

    # -----------------------------
    # STEP 7: Key sifting
    # -----------------------------

    alice_key, bob_key = sift_key(
        alice_bits,
        alice_bases,
        bob_bits,
        bob_bases
    )

    # -----------------------------
    # STEP 8: Calculate QBER
    # -----------------------------

    qber = calculate_qber(
        alice_key,
        bob_key
    )

    # -----------------------------
    # DISPLAY RESULTS
    # -----------------------------

    print("\n--- BB84 RESULTS ---")

    print("Number of Qubits:", number_of_bits)

    print("Alice Bits:")
    print(alice_bits)

    print("\nAlice Bases:")
    print(alice_bases)

    print("\nBob Bases:")
    print(bob_bases)

    print("\nAlice Sifted Key:")
    print(alice_key)

    print("\nBob Sifted Key:")
    print(bob_key)

    # Eve information
    print("\n--- EAVESDROPPER ---")

    if eve_attack:
        print("Eve Attack: ENABLED")
        print(
            f"Interception Rate: "
            f"{interception_rate * 100:.1f}%"
        )
        print("Intercepted States:", intercepted_count)

    else:
        print("Eve Attack: DISABLED")
        print("Intercepted States: 0")

    # Noise information
    print("\n--- CHANNEL NOISE ---")

    print(
        f"Noise Rate: "
        f"{noise_rate * 100:.1f}%"
    )

    print("Noise Errors:", noise_errors)

    # Key information
    print("\n--- SECURITY ANALYSIS ---")

    print("Final Key Length:", len(alice_key))

    print(
        f"QBER: "
        f"{qber * 100:.2f}%"
    )

    # Security decision
    if qber < 0.11:

        print("Key Status: ACCEPTED")
        print("Communication Status: SECURE")

    else:

        print("Key Status: REJECTED")
        print("Communication Status: ATTACK DETECTED")

    print("\n======================================")
    print("             PROCESS END")
    print("======================================")


# Run the program
if __name__ == "__main__":

    run_bb84(
        number_of_bits=1000,
        eve_attack=False,
        interception_rate=0.0,
        noise_rate=0.05
    )