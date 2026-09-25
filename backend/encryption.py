from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64


# -----------------------------------------
# AES ENCRYPTION
# -----------------------------------------

def encrypt_message(message, shared_secret):

    # AES requires a 16, 24, or 32 byte key.
    # We use the first 32 bytes of the PQC secret.
    key = shared_secret[:32]

    # Create AES-GCM object
    aes = AESGCM(key)

    # Generate a random 12-byte nonce
    nonce = os.urandom(12)

    # Convert message to bytes
    message_bytes = message.encode("utf-8")

    # Encrypt message
    ciphertext = aes.encrypt(
        nonce,
        message_bytes,
        None
    )

    # Combine nonce and ciphertext
    encrypted_data = nonce + ciphertext

    # Convert to Base64 for easy display/storage
    encoded_data = base64.b64encode(
        encrypted_data
    ).decode("utf-8")

    return encoded_data


# -----------------------------------------
# AES DECRYPTION
# -----------------------------------------

def decrypt_message(
    encrypted_data,
    shared_secret
):

    # Use the same 32-byte key
    key = shared_secret[:32]

    # Create AES-GCM object
    aes = AESGCM(key)

    # Decode Base64
    encrypted_bytes = base64.b64decode(
        encrypted_data
    )

    # Extract nonce
    nonce = encrypted_bytes[:12]

    # Extract ciphertext
    ciphertext = encrypted_bytes[12:]

    # Decrypt
    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode("utf-8")


# -----------------------------------------
# TEST ENCRYPTION
# -----------------------------------------

if __name__ == "__main__":

    print("\n======================================")
    print("       AES SECURE COMMUNICATION")
    print("======================================")

    # Test shared secret
    test_secret = os.urandom(32)

    # Message sent by Alice
    message = "Hello Bob! This is a quantum-safe message."

    print("\nOriginal Message:")
    print(message)

    # Encrypt
    encrypted = encrypt_message(
        message,
        test_secret
    )

    print("\nEncrypted Message:")
    print(encrypted)

    # Decrypt
    decrypted = decrypt_message(
        encrypted,
        test_secret
    )

    print("\nDecrypted Message:")
    print(decrypted)

    # Verify
    if message == decrypted:

        print("\nEncryption Verification: SUCCESS")

    else:

        print("\nEncryption Verification: FAILED")

    print("\n======================================")
    print("       ENCRYPTION COMPLETED")
    print("======================================")