import sys
import socket

server_address = 'localhost'
server_port = 5000

command = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((server_address, server_port))
    client_socket.send(command.encode('utf-8'))
