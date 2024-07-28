import socket

def generate_playfair_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = ''.join(sorted(set(key.upper()), key=key.index)).replace('J', 'I')
    matrix = ''
    for char in key + alphabet:
        if char not in matrix:
            matrix += char
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = text.upper().replace('J', 'I')
    text_pairs = [text[i:i+2] if i+1 < len(text) else text[i]+'X' for i in range(0, len(text), 2)]
    encrypted_text = []
    for pair in text_pairs:
        if len(pair) == 1:
            pair += 'X'
        row1, col1 = divmod(matrix.index(pair[0]), 5)
        row2, col2 = divmod(matrix.index(pair[1]), 5)
        if row1 == row2:
            encrypted_text.append(matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5])
        elif col1 == col2:
            encrypted_text.append(matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2])
        else:
            encrypted_text.append(matrix[row1][col2] + matrix[row2][col1])
    return ''.join(encrypted_text)

def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text_pairs = [text[i:i+2] for i in range(0, len(text), 2)]
    decrypted_text = []
    for pair in text_pairs:
        row1, col1 = divmod(matrix.index(pair[0]), 5)
        row2, col2 = divmod(matrix.index(pair[1]), 5)
        if row1 == row2:
            decrypted_text.append(matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5])
        elif col1 == col2:
            decrypted_text.append(matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2])
        else:
            decrypted_text.append(matrix[row1][col2] + matrix[row2][col1])
    return ''.join(decrypted_text)

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    command, text, key = request.split(':')
    if command == 'encrypt':
        response = playfair_encrypt(text, key)
    elif command == 'decrypt':
        response = playfair_decrypt(text, key)
    else:
        response = 'Invalid command'
    client_socket.send(response.encode())
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8085))
    server.listen(5)
    print('Done by 21BRS1378 SRIRAM VAISHNAV')
    print('Playfair Cipher Server listening on port 8085')
    while True:
        client_socket, addr = server.accept()
        handle_client(client_socket)

if __name__ == '__main__':
    main()
