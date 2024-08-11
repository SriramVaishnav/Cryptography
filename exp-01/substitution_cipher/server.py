import socket

def substitution_encrypt(text, shift):
    result = ''.join([chr((ord(char) - 97 + shift) % 26 + 97) if char.isalpha() else char for char in text])
    return result

def substitution_decrypt(text, shift):
    result = ''.join([chr((ord(char) - 97 - shift) % 26 + 97) if char.isalpha() else char for char in text])
    return result

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    command, text, shift = request.split(':')
    shift = int(shift)
    
    if command == 'encrypt':
        response = substitution_encrypt(text, shift)
    elif command == 'decrypt':
        response = substitution_decrypt(text, shift)
    else:
        response = 'Invalid command'
        
    client_socket.send(response.encode())
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    
    print("Done by 21BRS1378 SRIRAM VAISHNAV")
    print('Substitution Cipher Server listening on port 8080')
    
    while True:
        client_socket, addr = server.accept()
        handle_client(client_socket)

if __name__ == '__main__':
    main()
