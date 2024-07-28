import socket

def rail_fence_encrypt(text, key):
    rail = ['' for _ in range(key)]
    direction_down = False
    row = 0

    for char in text:
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        rail[row] += char
        row += 1 if direction_down else -1

    return ''.join(rail)

def rail_fence_decrypt(text, key):
    rail = [['\n' for _ in range(len(text))] for _ in range(key)]
    direction_down = None
    row, col = 0, 0

    for i in range(len(text)):
        if row == 0:
            direction_down = True
        if row == key - 1:
            direction_down = False
        rail[row][col] = '*'
        col += 1
        row += 1 if direction_down else -1

    index = 0
    for i in range(key):
        for j in range(len(text)):
            if (rail[i][j] == '*' and index < len(text)):
                rail[i][j] = text[index]
                index += 1

    result = []
    row, col = 0, 0
    for i in range(len(text)):
        if row == 0:
            direction_down = True
        if row == key - 1:
            direction_down = False
        if rail[row][col] != '*':
            result.append(rail[row][col])
        col += 1
        row += 1 if direction_down else -1

    return ''.join(result)

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    command, text, key = request.split(':')
    key = int(key)
    if command == 'encrypt':
        response = rail_fence_encrypt(text, key)
    elif command == 'decrypt':
        response = rail_fence_decrypt(text, key)
    else:
        response = 'Invalid command'
    client_socket.send(response.encode())
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8081))
    server.listen(5)
    print('Done by 21BRS1378 SRIRAM VAISHNAV')
    print('Rail-Fence Cipher Server listening on port 8081')
    while True:
        client_socket, addr = server.accept()
        handle_client(client_socket)

if __name__ == '__main__':
    main()
