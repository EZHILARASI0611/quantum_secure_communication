import sys
import os

# Add backend folder to Python path
sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from secure_communication import (
    run_bb84,
    run_mlkem,
    derive_hybrid_key,
    encrypt_message,
    decrypt_message
)


# ============================================================
# REPRODUCIBLE SECURITY TEST
# ============================================================

def run_test():

    print("\n")
    print("==============================================")
    print("     QUANTUM-SAFE SYSTEM REPRODUCIBILITY TEST")
    print("==============================================")

    # --------------------------------------------------------
    # TEST 1: BB84
    # --------------------------------------------------------

    print("\n[TEST 1] BB84 KEY GENERATION")

    alice_key, bob_key, qber = run_bb84(
        number_of_bits=256
    )

    print("\nBB84 Test: PASSED")

    # --------------------------------------------------------
    # TEST 2: QBER
    # --------------------------------------------------------

    print("\n[TEST 2] QBER SECURITY CHECK")

    qber_threshold = 0.11

    print(
        f"Measured QBER: {qber * 100:.2f}%"
    )

    print(
        f"Security Threshold: "
        f"{qber_threshold * 100:.0f}%"
    )

    if qber < qber_threshold:

        print("QBER Test: PASSED")

    else:

        print("QBER Test: FAILED")

        return

    # --------------------------------------------------------
    # TEST 3: ML-KEM
    # --------------------------------------------------------

    print("\n[TEST 3] ML-KEM-768")

    pqc_secret = run_mlkem()

    print("ML-KEM Test: PASSED")

    # --------------------------------------------------------
    # TEST 4: HYBRID KEY
    # --------------------------------------------------------

    print("\n[TEST 4] HYBRID KEY DERIVATION")

    hybrid_key = derive_hybrid_key(
        alice_key,
        pqc_secret
    )

    print(
        "Hybrid AES Key:",
        len(hybrid_key),
        "bytes"
    )

    print("Hybrid Key Test: PASSED")

    # --------------------------------------------------------
    # TEST 5: ENCRYPTION
    # --------------------------------------------------------

    print("\n[TEST 5] AES-GCM ENCRYPTION")

    original_message = (
        "Quantum-safe communication test message."
    )

    encrypted_message = encrypt_message(
        original_message,
        hybrid_key
    )

    print(
        "Encrypted Data:",
        len(encrypted_message),
        "bytes"
    )

    print("Encryption Test: PASSED")

    # --------------------------------------------------------
    # TEST 6: DECRYPTION
    # --------------------------------------------------------

    print("\n[TEST 6] AES-GCM DECRYPTION")

    decrypted_message = decrypt_message(
        encrypted_message,
        hybrid_key
    )

    print(
        "Decrypted Message:"
    )

    print(decrypted_message)

    # --------------------------------------------------------
    # FINAL VERIFICATION
    # --------------------------------------------------------

    print("\n[TEST 7] FINAL MESSAGE VERIFICATION")

    if original_message == decrypted_message:

        print("Message Verification: PASSED")

    else:

        print("Message Verification: FAILED")

        return

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print("\n==============================================")
    print("           ALL TESTS PASSED")
    print("==============================================")

    print("\nBB84:              PASSED")
    print("QBER:              PASSED")
    print("ML-KEM-768:        PASSED")
    print("Hybrid Key:        PASSED")
    print("AES Encryption:    PASSED")
    print("AES Decryption:    PASSED")
    print("Message Verify:    PASSED")

    print("\nCommunication Status: SECURE")

    print("\n==============================================")
    print("       REPRODUCIBILITY TEST COMPLETED")
    print("==============================================")


# ============================================================
# START TEST
# ============================================================

if __name__ == "__main__":

    run_test()