#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys

server_host = sys.argv[1]
server_port = int(sys.argv[2])

with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((server_host, server_port))

    while True:
        try:
            message = input('Client says: ')
            if not message:
                print('Shutting down')
                break

            client_socket.send(message.encode('utf-8'))

            answer = client_socket.recv(1024)
            if not answer:
                print('Disconnected from the server')
                break

            print(f"Server echoed: {answer.decode('utf-8')}")
        except socket.error:
            print('Disconnected from the server')
            break
