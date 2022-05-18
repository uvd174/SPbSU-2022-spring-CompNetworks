_places_in_number = 16
_bits_in_byte = 8
_bytes_in_number = _places_in_number // _bits_in_byte


def calculate_checksum(message: bytes):
    numbers = [
        int.from_bytes(message[i:i+_bytes_in_number], 'little')
        for i in range(0, len(message), _bytes_in_number)
    ]
    numbers_sum = sum(numbers) & ((1 << _places_in_number) - 1)
    checksum = ((1 << _places_in_number) - 1) - numbers_sum
    return checksum


def check_checksum(message: bytes, checksum: int):
    return calculate_checksum(message) == checksum
