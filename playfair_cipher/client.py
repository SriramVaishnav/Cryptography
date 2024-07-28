import socket

def send_request(command, text, key):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8085))
    request = f'{command}:{text}:{key}'
    client.send(request.encode())
    response = client.recv(4096).decode()
    print(f'Response: {response}')
    client.close()

if __name__ == '__main__':
    while True:
        command = input("Enter command (encrypt, decrypt): ")
        text = input("Enter text: ").upper().replace('J', 'I')
        key = input("Enter key: ").upper().replace('J', 'I')
        send_request(command, text, key)
