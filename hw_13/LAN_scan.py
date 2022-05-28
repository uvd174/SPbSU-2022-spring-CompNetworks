import socket
import sys
import netifaces
from ipaddress import ip_address
import getmac
from tqdm import tqdm


def get_network_prefix(ip: str, mask_size: int) -> str:
    ip = ip_address(ip)

    network_mask = (0xffffffff >> (32 - mask_size)) << (32 - mask_size)
    network_pref = int(ip) & network_mask
    return str(ip_address(network_pref))


def mac_for_ip(ip):
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        try:
            if_mac = addresses[netifaces.AF_LINK][0]['addr']
            if_ip = addresses[netifaces.AF_INET][0]['addr']
        except (IndexError, KeyError):
            if_mac = if_ip = None
        if if_ip == ip:
            return if_mac
    return None


def generate_ip_addresses(network_pref: str, mask_size: int):
    network_pref = ip_address(network_pref)
    for suffix in range(2 << (31 - mask_size)):
        generated_ip = ip_address(int(network_pref) + suffix)
        yield str(generated_ip)


network_mask_size = int(sys.argv[1])
assert 0 <= network_mask_size <= 32, 'Network mask size must be in range [0, 32]'

my_ip = socket.gethostbyname(socket.gethostname())
my_mac = mac_for_ip(my_ip)
my_hostname = socket.gethostname()

network_prefix = get_network_prefix(my_ip, network_mask_size)

print(f'My host:\nIP-address: {my_ip}; MAC-address: {my_mac}; Host name: {my_hostname}')
print(f'Network (CIDR={network_prefix}/{network_mask_size}):')

for generated_ip_address in tqdm(
        generate_ip_addresses(network_prefix, network_mask_size), total=(1 << (32 - network_mask_size))):
    if generated_ip_address == my_ip:
        continue

    received_mac = getmac.get_mac_address(ip=generated_ip_address)
    if received_mac:
        try:
            hostname = socket.gethostbyaddr(generated_ip_address)[0]
        except socket.error:
            hostname = 'Unknown'
        print(f' IP-address: {generated_ip_address}; MAC-address: {received_mac}; Host name: {hostname}')
