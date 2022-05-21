import sys
import socket


def get_reachable_ports(ip_addr, lower, upper, verbose=True):
    ports = []
    for port in range(lower, upper + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as testing_socket:
            testing_socket.settimeout(0.0001)
            if verbose:
                print(f'Checking port {port}... ', end='')
            try:
                testing_socket.connect((ip_addr, port))
                if verbose:
                    print('Fine!')
                ports.append(port)
            except socket.error as e:
                if verbose:
                    print('Error!')
                continue

    return ports


if __name__ == '__main__':
    ip_address = sys.argv[1]
    lower_bound, upper_bound = int(sys.argv[2]), int(sys.argv[3])
    assert lower_bound < upper_bound, 'The lower bound must be LOWER than the upper bound'
    print(get_reachable_ports(ip_address, lower_bound, upper_bound))
