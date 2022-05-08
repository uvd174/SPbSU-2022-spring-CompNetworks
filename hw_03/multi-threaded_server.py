#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import *
import os.path
import sys
from threading import Thread
from queue import Queue


def client_processing(connection_socket_):
    with connection_socket_:
        request = connection_socket_.recv(1024).decode('utf-8')
        requested_file = request[5:].split(' ')[0]
        print(f'Received request: {request}')
        file_path = os.path.join(os.path.curdir, requested_file)

        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                data = file.read()
            response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + data
        else:
            response = b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\nThe requested file is missing!'

        connection_socket_.sendall(response)


def socket_worker(jobs):
    while True:
        conn_socket = jobs.get()
        client_processing(conn_socket)
        jobs.task_done()


queue = Queue()

server_port = 5000
concurrency_level = int(sys.argv[1])

with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind(('', server_port))
    server_socket.listen(1)

    for _ in range(concurrency_level):
        thread = Thread(target=socket_worker, args=(queue,), daemon=True)
        thread.start()

    print('The server is ready to receive.')

    while True:
        connection_socket, address = server_socket.accept()
        queue.put(connection_socket)
