import socket

def row_transposition_encrypt(text, key):
    key_order = sorted(list(key))
    num_columns = len(key)
    num_rows = len(text) // num_columns + (1 if len(text) % num_columns != 0 else 0)
    padded_text = text.ljust(num_columns * num_rows)
    matrix = [padded_text[i:i + num_columns] for i in range(0, len(padded_text), num_columns)]
    ciphertext = ''.join([''.join([row[key.index(k)] for row in matrix]) for k in key_order])
    return ciphertext

def row_transposition_decrypt(text, key):
    key_order = sorted(list(key))
    num_columns = len(key)
    num_rows = len(text) // num_columns
    columns = [''.join([text[j] for j in range(i, len(text), num_columns)]) for i in range(num_columns)]
    matrix = ['' for _ in range(num_rows)]
    for i, k in enumerate(key_order):
        for j in range(num_rows):
            matrix[j] += columns[key.index(k)][j]
    plaintext = ''.join(matrix).rstrip()
    return plaintext

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    command, text, key = request.split(':')
    if command == 'encrypt':
        response = row_transposition_encrypt(text, key)
    elif command == 'decrypt':
        response = row_transposition_decrypt(text, key)
    else:
        response = 'Invalid command'
    client_socket.send(response.encode())
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8082))
    server.listen(5)
    print("Done by 21BRS1378 SRIRAM VAISHNAV")
    print('Row Transposition Cipher Server listening on port 8082')
    while True:
        client_socket, addr = server.accept()
        handle_client(client_socket)

if __name__ == '__main__':
    main()
