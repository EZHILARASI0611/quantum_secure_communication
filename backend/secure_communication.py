import hashlib
import os

import oqs

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from bb84 import (
    generate_bits,
    generate_bases,
    encode_bits,
    measure_states,
    sift_key,
    calculate_qber
)


# ============================================================
# STEP 1: BB84 KEY GENERATION
# ============================================================

def run_bb84(number_of_bits=256):

    print("\n--------------------------------------")
    print("STEP 1: BB84 KEY GENERATION")
    print("--------------------------------------")

    # Alice generates random bits and bases
    alice_bits = generate_bits(number_of_bits)
    alice_bases = generate_bases(number_of_bits)

    # Alice encodes the bits
    quantum_states = encode_bits(
        alice_bits,
        alice_bases
    )

    # Bob chooses random bases
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

    print("BB84 Qubits:", number_of_bits)
    print("Sifted Key Length:", len(alice_key))
    print(f"QBER: {qber * 100:.2f}%")

    return alice_key, bob_key, qber


# ============================================================
# STEP 2: CONVERT BB84 KEY TO BYTES
# ============================================================

def key_to_bytes(key):

    # Convert list such as [1,0,1,1,...]
    # into a byte representation.

    bit_string = "".join(
        str(bit)
        for bit in key
    )

    # Add padding so the length is divisible by 8
    while len(bit_string) % 8 != 0:
        bit_string += "0"

    key_bytes = int(
        bit_string,
        2
    ).to_bytes(
        len(bit_string) // 8,
        byteorder="big"
    )

    return key_bytes


# ============================================================
# STEP 3: ML-KEM POST-QUANTUM KEY EXCHANGE
# ============================================================

def run_mlkem():

    print("\n--------------------------------------")
    print("STEP 2: ML-KEM POST-QUANTUM CRYPTOGRAPHY")
    print("--------------------------------------")

    algorithm = "ML-KEM-768"

    print("Algorithm:", algorithm)

    # Create KEM object
    kem = oqs.KeyEncapsulation(
        algorithm
    )

    # Receiver generates key pair
    public_key = kem.generate_keypair()

    # Sender encapsulates a shared secret
    ciphertext, sender_secret = (
        kem.encap_secret(public_key)
    )

    # Receiver decapsulates
    receiver_secret = (
        kem.decap_secret(ciphertext)
    )

    # Verify both secrets match
    if sender_secret != receiver_secret:

        raise RuntimeError(
            "ML-KEM shared secret verification failed."
        )

    print("ML-KEM Key Exchange: SUCCESS")
    print(
        "Shared Secret Length:",
        len(sender_secret),
        "bytes"
    )

    return sender_secret


# ============================================================
# STEP 4: DERIVE HYBRID AES KEY
# ============================================================

def derive_hybrid_key(
    bb84_key,
    pqc_secret
):

    print("\n--------------------------------------")
    print("STEP 3: HYBRID KEY DERIVATION")
    print("--------------------------------------")

    bb84_bytes = key_to_bytes(
        bb84_key
    )

    # Combine BB84 key material and
    # post-quantum shared secret.
    combined_material = (
        bb84_bytes +
        pqc_secret
    )

    # SHA-256 produces a 32-byte key
    aes_key = hashlib.sha256(
        combined_material
    ).digest()

    print(
        "Hybrid AES Key Length:",
        len(aes_key),
        "bytes"
    )

    print("Hybrid Key Derivation: SUCCESS")

    return aes_key


# ============================================================
# STEP 5: AES-GCM ENCRYPTION
# ============================================================

def encrypt_message(
    message,
    aes_key
):

    print("\n--------------------------------------")
    print("STEP 4: AES-GCM ENCRYPTION")
    print("--------------------------------------")

    aes = AESGCM(
        aes_key
    )

    # Generate random nonce
    nonce = os.urandom(12)

    # Encrypt
    ciphertext = aes.encrypt(
        nonce,
        message.encode("utf-8"),
        None
    )

    encrypted_data = (
        nonce +
        ciphertext
    )

    print(
        "Message encrypted successfully."
    )

    return encrypted_data


# ============================================================
# STEP 6: AES-GCM DECRYPTION
# ============================================================

def decrypt_message(
    encrypted_data,
    aes_key
):

    print("\n--------------------------------------")
    print("STEP 5: AES-GCM DECRYPTION")
    print("--------------------------------------")

    aes = AESGCM(
        aes_key
    )

    # Extract nonce
    nonce = encrypted_data[:12]

    # Extract ciphertext
    ciphertext = encrypted_data[12:]

    # Decrypt
    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    message = plaintext.decode(
        "utf-8"
    )

    print(
        "Message decrypted successfully."
    )

    return message


# ============================================================
# COMPLETE HYBRID COMMUNICATION
# ============================================================

def secure_communication():

    print("\n")
    print("==============================================")
    print("   QUANTUM-SAFE SECURE COMMUNICATION SYSTEM")
    print("==============================================")

    # --------------------------------------------------------
    # STEP 1: BB84
    # --------------------------------------------------------

    alice_key, bob_key, qber = run_bb84(
        number_of_bits=256
    )

    # Security threshold
    qber_threshold = 0.11

    print("\nSecurity Threshold: 11%")

    if qber >= qber_threshold:

        print("\n❌ SECURITY CHECK FAILED")

        print(
            "QBER is too high."
        )

        print(
            "BB84 key rejected."
        )

        print(
            "Communication stopped."
        )

        return

    print("\n✅ BB84 SECURITY CHECK PASSED")

    # --------------------------------------------------------
    # STEP 2: ML-KEM
    # --------------------------------------------------------

    pqc_secret = run_mlkem()

    # --------------------------------------------------------
    # STEP 3: HYBRID KEY
    # --------------------------------------------------------

    hybrid_key = derive_hybrid_key(
        alice_key,
        pqc_secret
    )

    # --------------------------------------------------------
    # STEP 4: MESSAGE
    # --------------------------------------------------------

    message = (
        "Hello Bob! "
        "This message is protected using "
        "BB84 and post-quantum cryptography."
    )

    print("\nOriginal Message:")
    print(message)

    # --------------------------------------------------------
    # STEP 5: ENCRYPT
    # --------------------------------------------------------

    encrypted_message = encrypt_message(
        message,
        hybrid_key
    )

    print(
        "\nEncrypted Data Length:",
        len(encrypted_message),
        "bytes"
    )

    # --------------------------------------------------------
    # STEP 6: DECRYPT
    # --------------------------------------------------------

    decrypted_message = decrypt_message(
        encrypted_message,
        hybrid_key
    )

    print("\nDecrypted Message:")
    print(decrypted_message)

    # --------------------------------------------------------
    # FINAL VERIFICATION
    # --------------------------------------------------------

    print("\n--------------------------------------")
    print("FINAL SECURITY VERIFICATION")
    print("--------------------------------------")

    if message == decrypted_message:

        print("Message Verification: SUCCESS")
        print("Communication Status: SECURE")

    else:

        print("Message Verification: FAILED")
        print("Communication Status: NOT SECURE")

    print("\n==============================================")
    print("      HYBRID COMMUNICATION COMPLETED")
    print("==============================================")


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    secure_communication()