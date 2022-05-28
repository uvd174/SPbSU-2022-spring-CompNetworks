import random
import socket
import sys
from time import perf_counter
from ipaddress import ip_address
from typing import Tuple

TIMEOUT = 1


class ICMPMessage:
    message_type: int
    message_code: int
    _checksum: int
    rest: bytes
    data: bytes

    def __init__(self, message_type: int, message_code: int, rest: bytes, data: bytes):
        self.message_type = message_type
        self.message_code = message_code
        self._checksum = 0
        self.rest = rest
        self.data = data

        self._checksum = self.calculate_checksum()

    @classmethod
    def from_bytes(cls, packet: bytes) -> 'ICMPMessage':
        message_type = packet[0]
        message_code = packet[1]
        checksum = int.from_bytes(packet[2:4], 'big', signed=False)
        rest = packet[4:8]
        data = packet[8:]

        icmp_message = cls(message_type, message_code, rest, data)
        icmp_message._checksum = checksum
        return icmp_message

    def to_bytes(self) -> bytes:
        message_type_bytes = self.message_type.to_bytes(1, 'big', signed=False)
        message_code_bytes = self.message_code.to_bytes(1, 'big', signed=False)
        checksum_bytes = self._checksum.to_bytes(2, 'big', signed=False)
        message_bytes = message_type_bytes + message_code_bytes + checksum_bytes + self.rest + self.data
        return message_bytes

    @property
    def checksum(self) -> int:
        return self._checksum

    def calculate_checksum(self) -> int:
        message_bytes = bytearray(self.to_bytes())
        message_bytes[2], message_bytes[3] = 0, 0
        if len(message_bytes) % 2:
            message_bytes += b'\x00'

        checksum_mask = (1 << 16) - 1

        numbers = [
            int.from_bytes(message_bytes[i:i+2], 'big', signed=False)
            for i in range(0, len(message_bytes), 2)
        ]
        numbers_sum = sum(numbers)

        while numbers_sum >> 16:
            numbers_sum = (numbers_sum & checksum_mask) + (numbers_sum >> 16)

        return checksum_mask - numbers_sum

    def check_checksum(self) -> bool:
        return self.calculate_checksum() == self._checksum


def get_name_and_host(name_or_host: str) -> Tuple[str, str]:
    try:
        ip_address(name_or_host)
        server_host = name_or_host
    except ValueError:
        server_name = name_or_host
        try:
            server_host = socket.gethostbyname(server_name)
        except socket.error:
            server_host = None
    else:
        try:
            server_name = socket.gethostbyaddr(server_host)[0]
        except socket.herror:
            server_name = None

    return server_name, server_host


if __name__ == '__main__':
    traceroute_id = random.randint(0, (1 << 16) - 1)

    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as client_socket:
        client_socket.settimeout(TIMEOUT)

        target_server = sys.argv[1]
        number_of_messages = int(sys.argv[2])
        max_hops = int(sys.argv[3])

        target_server_name, target_server_host = get_name_and_host(target_server)
        if not target_server_host:
            print(f'Unable to resolve target system name {target_server_name}.')
            sys.exit(0)

        if target_server_name:
            print(f'Tracing route to {target_server_name} [{target_server_host}]')
        else:
            print(f'Tracing route to {target_server_host}')
        print(f'over a maximum of {max_hops} hops:\n')

        sequence_number = 0
        target_reached = False

        for ttl in range(1, max_hops + 1):
            client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl.to_bytes(1, 'big', signed=False))
            print(f"{str(ttl).rjust(3, ' ')}", end=' ')

            current_server_name, current_server_host = None, None

            for message_index in range(number_of_messages):
                sequence_number += 1
                start = perf_counter()
                message = ICMPMessage(
                    8,
                    0,
                    traceroute_id.to_bytes(2, 'big', signed=False) + sequence_number.to_bytes(2, 'big', signed=False),
                    bytearray([0] * 32),
                )
                client_socket.sendto(message.to_bytes(), (target_server_host, 1))

                try:
                    response_message, current_server_address = client_socket.recvfrom(1024)
                    icmp_response = ICMPMessage.from_bytes(response_message[20:])

                    current_server_host = current_server_address[0]
                    finish = perf_counter()

                    if icmp_response.message_type == 0:
                        target_reached = True

                    rtt = round((finish - start) * 1000)
                    print(f"{str(rtt).rjust(5, ' ')} ms", end=' ')

                except socket.timeout as exc:
                    print('    *   ', end=' ')

            if current_server_host:
                current_server_name, current_server_host = get_name_and_host(current_server_host)

            if current_server_name:
                print(f' {current_server_name} [{current_server_host}]')
            elif current_server_host:
                print(f' {current_server_host}')
            else:
                print(' Request timed out.')

            if target_reached:
                break

    print('\nTrace complete.')
