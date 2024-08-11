import socket

def send_request(command, text, shift):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))
    
    request = f'{command}:{text}:{shift}'
    client.send(request.encode())
    
    response = client.recv(4096).decode()
    print(f'Response: {response}')
    
    client.close()

if __name__ == '__main__':
    while True:
        command = input("Enter command (encrypt, decrypt): ")
        text = input("Enter text: ")
        shift = input("Enter shift: ")
        send_request(command, text, shift)
