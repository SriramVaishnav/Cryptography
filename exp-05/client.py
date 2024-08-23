import socket

def rsa_encrypt(number, public_key):
    exponent, modulus = public_key
    ciphertext = pow(number, exponent, modulus)
    return ciphertext

def start_client():
    host = '127.0.0.1'
    port = 65432
    
    client_socket = socket.socket()
    client_socket.connect((host, port))
    
    public_key = client_socket.recv(1024).decode()
    public_key = eval(public_key)
    
    number_to_encrypt = int(input("Enter an integer to encrypt: "))
    encrypted_number = rsa_encrypt(number_to_encrypt, public_key)
    
    client_socket.send(str(encrypted_number).encode())
    
    decrypted_response = client_socket.recv(1024).decode()
    print(f"Decrypted integer from server: {decrypted_response}")
    
    client_socket.close()

if __name__ == "__main__":
    start_client()
