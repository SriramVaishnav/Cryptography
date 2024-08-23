import socket
import random

def calculate_gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def create_rsa_keys():
    prime1 = 29
    prime2 = 53
    modulus = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    
    exponent = random.randrange(2, totient)
    while calculate_gcd(exponent, totient) != 1:
        exponent = random.randrange(2, totient)
    
    d_value = pow(exponent, -1, totient)
    
    return (exponent, modulus), (d_value, modulus)

def rsa_decrypt(ciphertext, private_key):
    d_value, modulus = private_key
    decrypted_message = pow(ciphertext, d_value, modulus)
    return decrypted_message

def start_server():
    host = '127.0.0.1'
    port = 65432
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    
    public_key, private_key = create_rsa_keys()
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")
    
    connection, address = server_socket.accept()
    print(f"Connection from: {address}")
    
    connection.send(str(public_key).encode())
    encrypted_msg = int(connection.recv(1024).decode())
    print(f"Received encrypted integer: {encrypted_msg}")
    
    decrypted_msg = rsa_decrypt(encrypted_msg, private_key)
    print(f"Decrypted integer: {decrypted_msg}")
    
    connection.send(str(decrypted_msg).encode())
    connection.close()

if __name__ == "__main__":
    start_server()
