from socket import *
import os.path

server_port = 5000

with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind(('', server_port))
    server_socket.listen(1)
    print('The server is ready to receive.')

    while True:
        connection_socket, address = server_socket.accept()

        with connection_socket:

            request = connection_socket.recv(1024).decode('utf-8')
            requested_file = request[5:].split(' ')[0]
            print(f'Received request: {request}')
            file_path = os.path.join(os.path.curdir, requested_file)

            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    data = file.read()
                response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + data
            else:
                response = b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\nThe requested file is missing!'

            connection_socket.send(response)
