from checksum import calculate_checksum, check_checksum
from random import random


def encode_packet(state: int, data: bytes):
    state = b'\x01' if state else b'\x00'
    data_checksum = calculate_checksum(state + data)
    packet = data_checksum.to_bytes(2, 'little') + state + data
    return packet


def decode_packet(frame: bytes):
    data_checksum = int.from_bytes(frame[:2], 'little')
    state = frame[2]
    data = frame[3:]
    is_fine = check_checksum(frame[2:], data_checksum)
    return state, data, is_fine


def error_occurred(error_rate: float):
    return random() < error_rate
