import socket
from time import sleep

from utils import error_occurred, encode_packet, decode_packet
import sys


server_host = sys.argv[1]
server_port = int(sys.argv[2])
timeout = float(sys.argv[3])

server_address = (server_host, server_port)

error_rate = 0.3
chunk_size = 150


def receive_message():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        try:
            server_socket.bind(server_address)
        except socket.error:
            print('Cannot open a socket')
            return None, None

        print(f'The server is listening at port {server_port}')
        received_text = ''
        current_state = 0

        while True:
            packet, client_address = server_socket.recvfrom(1024)
            state, data, is_fine = decode_packet(packet)

            print(f'Received {data} {state}')

            if not is_fine:
                continue

            if not error_occurred(error_rate):
                server_socket.sendto(bytearray([state]), client_address)
            print(f'Sent ACK{state}')

            if state != current_state:
                continue
            current_state = 1 - current_state

            if not len(data):
                break

            received_text += data.decode('utf-8')

        print('\nReceived text:\n' + received_text)

    return received_text, client_address


def send_message(client_address, message):
    message_chunks = [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]
    message_chunks.append('')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.settimeout(timeout)
        current_state = 0

        for chunk in message_chunks:
            packet = encode_packet(current_state, chunk.encode('utf-8'))

            while True:
                if not error_occurred(error_rate):
                    server_socket.sendto(packet, client_address)
                print(f'Sent {chunk.encode("utf-8")} {current_state}')

                try:
                    ack_packet, _ = server_socket.recvfrom(1024)
                except socket.timeout:
                    continue
                except socket.error:
                    print('Disconnected from client')
                    return

                server_state = ack_packet[0]
                print(f'Received ACK{server_state}')
                if server_state != current_state:
                    continue

                current_state = 1 - current_state
                break


if __name__ == '__main__':
    text, client_addr = receive_message()
    sleep(4)
    if text and client_addr:
        send_message(client_addr, text)
