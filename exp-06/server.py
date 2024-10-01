import socket
import random
import threading

p = 23 
g = 5   

clients = {}
public_keys = {}

def handle_client(conn, addr, client_id):
    print(f"Connected to {addr}")

    private_key = random.randint(1, p - 1)

    public_key = pow(g, private_key, p)

    conn.send(str(public_key).encode())

    client_public_key = int(conn.recv(1024).decode())
    public_keys[client_id] = client_public_key

    if len(public_keys) < 3:
        conn.send("Waiting for other clients...".encode())
    else:
        conn.send("All clients connected.".encode())

    shared_secret_AB = pow(public_keys[2], private_key, p)
    shared_secret_BC = pow(public_keys[3], private_key, p)
    shared_secret_CA = pow(public_keys[1], private_key, p)
    common_secret_ABC = pow(shared_secret_AB, private_key, p)

    conn.send(f"Common shared secret: {common_secret_ABC}".encode())
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9999))
    server.listen(5)
    print("Server started and listening on port 9999")

    client_id = 1
    while True:
        conn, addr = server.accept()
        clients[client_id] = conn
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_id))
        thread.start()
        client_id += 1

start_server()
