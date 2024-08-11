import socket
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999)) 
    message = "HelloWorld"
    client.sendall(f'encrypt:{message}'.encode('utf-8'))
    encrypted_message = client.recv(1024).decode('utf-8')
    print(f"Encrypted: {encrypted_message}")
    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    client.sendall(f'decrypt:{encrypted_message}'.encode('utf-8'))
    decrypted_message = client.recv(1024).decode('utf-8')
    print(f"Decrypted: {decrypted_message}")
    client.close()

if __name__ == "__main__":
    main()