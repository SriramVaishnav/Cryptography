import socket

def create_key_matrix(key, size):
    key_matrix = [[0] * size for _ in range(size)]
    k = 0
    for i in range(size):
        for j in range(size):
            key_matrix[i][j] = ord(key[k]) % 65
            k += 1
    return key_matrix

def matrix_mult(A, B, size):
    result = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(size)) % 26
    return result

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def invert_matrix(matrix, size):
    def determinant(mat, n):
        if n == 1:
            return mat[0][0]
        if n == 2:
            return (mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]) % 26
        det = 0
        for c in range(n):
            sub_matrix = [row[:c] + row[c+1:] for row in mat[1:]]
            sign = (-1) ** (c % 2)
            det = (det + sign * mat[0][c] * determinant(sub_matrix, n - 1)) % 26
        return det
    
    det = determinant(matrix, size)
    det_inv = mod_inverse(det, 26)
    adjugate = [[0] * size for _ in range(size)]
    
    for i in range(size):
        for j in range(size):
            minor = [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]
            adjugate[j][i] = (det_inv * determinant(minor, size - 1)) % 26
    return adjugate

def encrypt(text, key):
    size = int(len(key) ** 0.5)
    key_matrix = create_key_matrix(key, size)
    text = [ord(char) % 65 for char in text.upper()]
    while len(text) % size != 0:
        text.append(ord('X') % 65)
    text_matrix = [text[i:i+size] for i in range(0, len(text), size)]
    encrypted_matrix = [matrix_mult(key_matrix, [row], size)[0] for row in text_matrix]
    encrypted_text = ''.join(chr(num + 65) for row in encrypted_matrix for num in row)
    return encrypted_text

def decrypt(text, key):
    size = int(len(key) ** 0.5)
    key_matrix = create_key_matrix(key, size)
    inverse_key_matrix = invert_matrix(key_matrix, size)
    text = [ord(char) % 65 for char in text.upper()]
    text_matrix = [text[i:i+size] for i in range(0, len(text), size)]
    decrypted_matrix = [matrix_mult(inverse_key_matrix, [row], size)[0] for row in text_matrix]
    decrypted_text = ''.join(chr(num + 65) for row in decrypted_matrix for num in row)
    return decrypted_text

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    try:
        command, text, key = request.split(':')
        if command == 'encrypt':
            response = encrypt(text, key)
        elif command == 'decrypt':
            response = decrypt(text, key)
        else:
            response = 'Invalid command'
    except Exception as e:
        response = f'Error: {str(e)}'
    
    client_socket.send(response.encode())
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8086))
    server.listen(5)
    print('Done by 21BRS1378 SRIRAM VAISHNAV')
    print('Hill Cipher Server listening on port 8086')
    
    while True:
        client_socket, addr = server.accept()
        handle_client(client_socket)

if __name__ == '__main__':
    main()