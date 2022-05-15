#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import random

server_port = 5000
error_rate = 0.2

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind(('', server_port))
    print('The server is ready to receive.')

    while True:
        message, client_address = server_socket.recvfrom(1024)

        error_occurred = random.random() < error_rate
        if error_occurred:
            continue

        print('Received:', message.decode('utf-8'))
        modified_message = message.decode('utf-8').upper()
        server_socket.sendto(modified_message.encode('utf-8'), client_address)
