#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys
from time import perf_counter


server_host = sys.argv[1]
server_port = sys.argv[2]

server_address = (server_host, int(server_port))
request_number = 10
timeout = 1.0
client_message = b'pingpingpingpingpingpingpingping'

rtts = []

print(f'Pinging {server_host} with {len(client_message)} bytes of data:')

for request_index in range(1, request_number+1):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(timeout)

        start_time = perf_counter()
        client_socket.sendto(client_message, server_address)
        try:
            response, address = client_socket.recvfrom(1024)
            finish_time = perf_counter()
            elapsed_time = round(finish_time - start_time, 7)
            rtts.append(elapsed_time)
            print(f'Reply from {address[0]}: bytes={len(response)} time={elapsed_time}s')
        except socket.timeout:
            print('Request timed out')

lost_packets = request_number - len(rtts)

print(f"""
Ping statistics for {server_host}:
    Packets: Sent = {request_number}, Received = {len(rtts)}, Lost = {lost_packets} ({round((lost_packets / request_number)*100)}% loss),
Approximate round trip times in seconds:
    Minimum = {min(rtts)}s, Maximum = {max(rtts)}s, Average = {round(sum(rtts)/len(rtts), 7)}s
""")
