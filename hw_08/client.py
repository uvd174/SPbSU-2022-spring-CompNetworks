import socket
from utils import error_occurred, encode_packet, decode_packet
import sys


server_host = sys.argv[1]
server_port = int(sys.argv[2])
timeout = float(sys.argv[3])

server_address = (server_host, server_port)

error_rate = 0.3
chunk_size = 150

with open('sample_text.txt', 'rt') as text_file:
    sample_text = text_file.read()


def receive_message(client_address):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.bind(client_address)
        print(f'Started listening messages at port {client_address[1]}')
        received_text = ''
        current_state = 0

        while True:
            packet, server_addr = client_socket.recvfrom(1024)
            state, data, is_fine = decode_packet(packet)

            print(f'Received {data} {state}')

            if not is_fine:
                continue

            if not error_occurred(error_rate):
                client_socket.sendto(bytearray([state]), server_addr)
            print(f'Sent ACK{state}')

            if state != current_state:
                continue
            current_state = 1 - current_state

            if not len(data):
                break

            received_text += data.decode('utf-8')

        print('\nReceived text:\n' + received_text)

    return received_text, client_address


def send_message(server_addr, message):
    message_chunks = [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]
    message_chunks.append('')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(timeout)
        current_state = 0

        for chunk in message_chunks:
            packet = encode_packet(current_state, chunk.encode('utf-8'))

            while True:
                if not error_occurred(error_rate):
                    client_socket.sendto(packet, server_addr)
                    client_addr = client_socket.getsockname()
                print(f'Sent {chunk.encode("utf-8")} {current_state}')

                try:
                    ack_packet, _ = client_socket.recvfrom(1024)
                except socket.timeout:
                    continue
                except socket.error:
                    print('Disconnected from server')
                    return client_addr

                server_state = ack_packet[0]
                print(f'Received ACK{server_state}')
                if server_state != current_state:
                    continue

                current_state = 1 - current_state
                break
        return client_addr


if __name__ == '__main__':
    client_address = send_message(server_address, sample_text)
    text, _ = receive_message(client_address)
