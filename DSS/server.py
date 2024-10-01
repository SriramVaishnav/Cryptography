from crypto_helpers import ElGamal, AES128, sha512, mod_exp

p = 2357  # A large prime number (for simplicity, use small for demo)
g = 2     # A generator for the group
y = mod_exp(g, 1751, p)  # Public key

# AES Key
aes_key = "thisisasecretkey"  # 16-byte AES key (128-bit)

def server_receive_message():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 8080))
        server_socket.listen()
        print("Server is listening on port 8080...")
        
        conn, addr = server_socket.accept()
        with conn:
            print('Connected by', addr)
            data = conn.recv(1024).decode('utf-8')
            
            # Verify the received data is correct
            print(f"Received Data: {data}")
            
            # Step 1: Split the encrypted message, r, and s
            encrypted_message, r, s = data.split(',')
            r = int(r)  # Convert back to integers
            s = int(s)  # Convert back to integers
            
            print(f"Encrypted Message: {encrypted_message}")
            print(f"Signature: r={r}, s={s}")
            
            # Step 2: Decrypt the message using AES-128
            aes = AES128(aes_key)
            decrypted_message = aes.decrypt(encrypted_message)
            print(f"Decrypted Message: {decrypted_message}")
            
            # Step 3: Hash the decrypted message using SHA-512
            message_hash = sha512(decrypted_message)
            print(f"SHA-512 Hash: {message_hash}")
            
            # Step 4: Verify the ElGamal signature
            elgamal = ElGamal(p, g, 1751)
            if elgamal.verify(message_hash, r, s):
                print("Signature is valid. Non-repudiation ensured.")
            else:
                print("Invalid signature. Non-repudiation failed.")

if __name__ == "__main__":
    server_receive_message()
