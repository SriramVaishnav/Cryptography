from crypto_helpers import ElGamal, AES128, sha512

# ElGamal parameters (shared between client and server)
p = 2357  # A large prime number (for simplicity, use small for demo)
g = 2  # A generator for the group
x = 1751  # Private key

# AES Key
aes_key = "thisisasecretkey"  # 16-byte AES key (128-bit)

def client_send_message(message):
    # Step 1: Hash the message using SHA-512
    message_hash = sha512(message)
    print(f"SHA-512 Hash: {message_hash}")
    
    # Step 2: ElGamal Signing
    elgamal = ElGamal(p, g, x)
    r, s = elgamal.sign(message_hash)
    print(f"Signature: r={r}, s={s}")
    
    # Step 3: AES-128 Encryption
    aes = AES128(aes_key)
    encrypted_message = aes.encrypt(message)
    print(f"Encrypted Message: {encrypted_message}")
    
    # Step 4: Send encrypted message and signature to server
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 8080))
        # Send the encrypted message and signature as a comma-separated string
        data = f"{encrypted_message},{r},{s}"
        print(f"Sending Data: {data}")
        client_socket.sendall(data.encode('utf-8'))
        print("Message sent to server.")

if __name__ == "__main__":
    message = "This is a confidential message!"
    client_send_message(message)
