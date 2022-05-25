#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys
import threading

server_port = int(sys.argv[1])


def server_thread(conn_socket, host, port):
    with conn_socket:
        while True:
            message = conn_socket.recv(1024)
            if not message:
                conn_socket.shutdown(1)
                print(f'Closing the connection with [{host}]:{port}')
                break

            print(f"Received {message.decode('utf-8')} from [{host}]:{port}")

            response = message.decode('utf-8').upper()

            conn_socket.send(response.encode('utf-8'))
            print(f"Sent {response} to [{host}]:{port}")


with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('', server_port))
    server_socket.listen()
    print(f'The server is listening at {server_socket.getsockname()}{server_port}.')

    while True:
        connection_socket, client_address = server_socket.accept()
        client_host, client_port = client_address[0], client_address[1]
        print(f'Received connection from [{client_host}]:{client_port}')
        threading.Thread(target=server_thread, args=(connection_socket, client_host, client_port)).start()
