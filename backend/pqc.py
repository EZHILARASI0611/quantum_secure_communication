import oqs


# -----------------------------------------
# POST-QUANTUM CRYPTOGRAPHY - ML-KEM
# -----------------------------------------

def generate_pqc_keys():

    print("\n======================================")
    print("   POST-QUANTUM CRYPTOGRAPHY")
    print("======================================")

    # ML-KEM-768 is a standardized
    # post-quantum key encapsulation mechanism
    algorithm = "ML-KEM-768"

    print("\nAlgorithm:", algorithm)

    # Create ML-KEM object
    kem = oqs.KeyEncapsulation(algorithm)

    # Generate public and secret keys
    public_key = kem.generate_keypair()

    secret_key = kem.export_secret_key()

    print("\nKey Generation Completed")

    print(
        "Public Key Length:",
        len(public_key),
        "bytes"
    )

    print(
        "Secret Key Length:",
        len(secret_key),
        "bytes"
    )

    # -----------------------------------------
    # ENCAPSULATION
    # -----------------------------------------

    ciphertext, shared_secret_sender = (
        kem.encap_secret(public_key)
    )

    print("\nEncapsulation Completed")

    print(
        "Ciphertext Length:",
        len(ciphertext),
        "bytes"
    )

    # -----------------------------------------
    # DECAPSULATION
    # -----------------------------------------

    shared_secret_receiver = (
        kem.decap_secret(ciphertext)
    )

    print("\nDecapsulation Completed")

    # -----------------------------------------
    # VERIFY SHARED SECRET
    # -----------------------------------------

    if shared_secret_sender == shared_secret_receiver:

        print("\nShared Secret Verification: SUCCESS")

        print(
            "Sender and Receiver have the same secret."
        )

    else:

        print("\nShared Secret Verification: FAILED")

    print("\n======================================")
    print("       PQC PROCESS COMPLETED")
    print("======================================")


# -----------------------------------------
# START PROGRAM
# -----------------------------------------

if __name__ == "__main__":

    generate_pqc_keys()