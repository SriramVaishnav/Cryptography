import socket

def vigenere_encrypt(text, key):
    encrypted_text = []
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    text_int = [ord(i) for i in text]
    for i in range(len(text_int)):
        if text[i].isalpha():
            value = (text_int[i] + key_as_int[i % key_length]) % 26
            encrypted_text.append(chr(value + 65))
        else:
            encrypted_text.append(text[i])
    return ''.join(encrypted_text)

def vigenere_decrypt(text, key):
    decrypted_text = []
    key_length = len(key)
    key_as_int = [ord(i) for i in key]
    text_int = [ord(i) for i in text]
    for i in range(len(text_int)):
        if text[i].isalpha():
            value = (text_int[i] - key_as_int[i % key_length]) % 26
            decrypted_text.append(chr(value + 65))
        else:
            decrypted_text.append(text[i])
    return ''.join(decrypted_text)

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    command, text, key = request.split(':')
    key = key.upper()  # Ensure the key is in uppercase
    text = text.upper()  # Ensure the text is in uppercase
    if command == 'encrypt':
        response = vigenere_encrypt(text, key)
    elif command == 'decrypt':
        response = vigenere_decrypt(text, key)
    else:
        response = 'Invalid command'
    client_socket.send(response.encode())
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8083))
    server.listen(5)
    print('Done by 21BRS1378 SRIRAM VAISHNAV')
    print('Vigenère Cipher Server listening on port 8083')
    while True:
        client_socket, addr = server.accept()
        handle_client(client_socket)

if __name__ == '__main__':
    main()
