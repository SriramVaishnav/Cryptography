import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def generate_rsa_key_pair(key_size=2048):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def generate_aes_key():
    return os.urandom(32)  # 256-bit key

def encrypt_with_aes(key, plaintext):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return iv + ciphertext

def encrypt_with_rsa(public_key, data):
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def hybrid_encrypt(public_key, plaintext):
    aes_key = generate_aes_key()
    encrypted_data = encrypt_with_aes(aes_key, plaintext)
    encrypted_aes_key = encrypt_with_rsa(public_key, aes_key)
    return encrypted_aes_key, encrypted_data

# Generate RSA key pair
private_key, public_key = generate_rsa_key_pair()

# Generate 1024 bytes of random data as plaintext
plaintext = os.urandom(1024)

# Perform hybrid encryption
encrypted_aes_key, encrypted_data = hybrid_encrypt(public_key, plaintext)

def decrypt_with_rsa(private_key, encrypted_data):
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_with_aes(key, encrypted_data):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

def hybrid_decrypt(private_key, encrypted_aes_key, encrypted_data):
    aes_key = decrypt_with_rsa(private_key, encrypted_aes_key)
    plaintext = decrypt_with_aes(aes_key, encrypted_data)
    return plaintext

print(f"Plaintext length: {len(plaintext)} bytes")
print(f"Encrypted AES key length: {len(encrypted_aes_key)} bytes")
print(f"Encrypted data length: {len(encrypted_data)} bytes")

print("\nEncrypted AES Key (hex):")
print(encrypted_aes_key.hex())

print("\nEncrypted Data (first 100 bytes, hex):")
print(encrypted_data[:100].hex())

# Decryption
decrypted_data = hybrid_decrypt(private_key, encrypted_aes_key, encrypted_data)
print(f"Decrypted data length: {len(decrypted_data)} bytes")

print("\nDecrypted Data (first 100 bytes, hex):")
print(decrypted_data[:100].hex())

# Verify the decryption
if decrypted_data == plaintext:
    print("\nDecryption successful! The decrypted data matches the original plaintext.")
else:
    print("\nDecryption failed. The decrypted data does not match the original plaintext.")
