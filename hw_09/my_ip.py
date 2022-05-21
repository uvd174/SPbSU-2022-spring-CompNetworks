from netifaces import interfaces, ifaddresses, AF_INET
import socket

for interface in interfaces():
    addresses = ifaddresses(interface)
    if AF_INET in addresses and addresses[AF_INET][0]['addr'] != socket.gethostbyname('localhost'):
        print(f"My IP-address: {addresses[AF_INET][0]['addr']};\nmy network mask: {addresses[AF_INET][0]['netmask']}.")
