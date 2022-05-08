#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *
import sys

server_host = sys.argv[1]
server_port = sys.argv[2]
file_name = sys.argv[3]

request_message = f'GET /{file_name} HTTP/1.1\r\nHost: {server_host}:{server_port}\r\n\r\n'

with socket(AF_INET, SOCK_STREAM) as client_socket:
    client_socket.connect((server_host, int(server_port)))
    client_socket.send(request_message.encode('utf-8'))

    response = client_socket.recv(1024)

print(response.decode('utf-8'))
