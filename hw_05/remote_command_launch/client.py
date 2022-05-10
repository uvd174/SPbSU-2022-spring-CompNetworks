import sys
from socket import *

server_address = 'localhost'
server_port = 5000

with socket(AF_INET, SOCK_STREAM) as client_socket:
    client_socket.connect((server_address, server_port))
    command = sys.argv[1]
    client_socket.send(command.encode('utf-8'))
