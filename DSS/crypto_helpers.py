import random
import hashlib

# Helper functions
def mod_exp(base, exp, mod):
    """Performs modular exponentiation (base^exp % mod)."""
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def gcd(a, b):
    """Returns the greatest common divisor of a and b."""
    while b != 0:
        a, b = b, a % b
    return a

def find_mod_inverse(a, m):
    """Returns the modular inverse of a % m."""
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# SHA-512 Hash function
def sha512(message):
    """Returns SHA-512 hash of a message."""
    return hashlib.sha512(message.encode('utf-8')).hexdigest()

# AES-128 Encryption without libraries
class AES128:
    def __init__(self, key):
        self.key = self.key_expansion(key)

    def key_expansion(self, key):
        """Expand the 128-bit key (16 bytes) into a larger key."""
        # Placeholder for key expansion logic (implementing full AES-128 key expansion)
        return key

    def encrypt(self, plaintext):
        """Encrypts a 16-byte block of plaintext."""
        # Placeholder for AES encryption rounds
        return plaintext

    def decrypt(self, ciphertext):
        """Decrypts a 16-byte block of ciphertext."""
        # Placeholder for AES decryption rounds
        return ciphertext

# ElGamal Signature
class ElGamal:
    def __init__(self, p, g, x):
        self.p = p  # large prime
        self.g = g  # generator
        self.x = x  # private key
        self.y = mod_exp(g, x, p)  # public key (g^x mod p)

    def sign(self, message_hash):
        """Signs the message hash using ElGamal signature scheme."""
        k = random.randint(1, self.p - 2)
        while gcd(k, self.p - 1) != 1:
            k = random.randint(1, self.p - 2)
        r = mod_exp(self.g, k, self.p)
        k_inv = find_mod_inverse(k, self.p - 1)
        s = (k_inv * (int(message_hash, 16) - self.x * r)) % (self.p - 1)
        return (r, s)

    def verify(self, message_hash, r, s):
        """Verifies the ElGamal signature."""
        left = mod_exp(self.y, r, self.p) * mod_exp(r, s, self.p) % self.p
        right = mod_exp(self.g, int(message_hash, 16), self.p)
        return left == right
