import socket

def caesar_encrypt(text, shift):
    encrypted_text = ''.join(
        chr((ord(char) - 65 + shift) % 26 + 65) if char.isupper() else
        chr((ord(char) - 97 + shift) % 26 + 97) if char.islower() else char
        for char in text
    )
    return encrypted_text

def caesar_decrypt(text, shift):
    decrypted_text = ''.join(
        chr((ord(char) - 65 - shift) % 26 + 65) if char.isupper() else
        chr((ord(char) - 97 - shift) % 26 + 97) if char.islower() else char
        for char in text
    )
    return decrypted_text

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    command, text, shift = request.split(':')
    shift = int(shift)
    if command == 'encrypt':
        response = caesar_encrypt(text, shift)
    elif command == 'decrypt':
        response = caesar_decrypt(text, shift)
    else:
        response = 'Invalid command'
    client_socket.send(response.encode())
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8084))
    server.listen(5)
    print("Done by 21BRS1378 SRIRAM VAISHNAV")
    print('Caesar Cipher Server listening on port 8084')
    while True:
        client_socket, addr = server.accept()
        handle_client(client_socket)

if __name__ == '__main__':
    main()
