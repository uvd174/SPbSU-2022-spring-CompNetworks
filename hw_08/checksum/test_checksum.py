from checksum import calculate_checksum, check_checksum


def test_calculate_checksum_1():
    message = b'\xff\xff\x00\x00'
    assert calculate_checksum(message) == 0


def test_calculate_checksum_2():
    message = b'\xff\xff\x01\x00'
    assert not calculate_checksum(message) == 0


def test_check_checksum_1():
    message = b'\xff\xff\x00\x00'
    checksum = 0
    assert check_checksum(message, checksum)


def test_check_checksum_2():
    message = b'\xff\xff\x01\x00'
    checksum = 0
    assert not check_checksum(message, checksum)


def test_check_checksum_empty():
    message = b''
    checksum = (1 << 16) - 1
    assert check_checksum(message, checksum)


if __name__ == '__main__':
    test_calculate_checksum_1()
    test_calculate_checksum_2()
    test_check_checksum_1()
    test_check_checksum_2()
    test_check_checksum_empty()
