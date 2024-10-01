import socket
import random

# Large prime number (p) and primitive root (g) for the group
p = 23  # Example prime number
g = 5   # Example primitive root

def client_program():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9999))

    server_public_key = int(client.recv(1024).decode())
    print(f"Server's public key: {server_public_key}")

    private_key = random.randint(1, p - 1)

    public_key = pow(g, private_key, p)

    client.send(str(public_key).encode())

    shared_secret = pow(server_public_key, private_key, p)
    print(f"Shared secret with server: {shared_secret}")

    common_secret_msg = client.recv(1024).decode()
    print(common_secret_msg)

    client.close()

client_program()