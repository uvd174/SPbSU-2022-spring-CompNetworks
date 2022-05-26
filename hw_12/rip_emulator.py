import json
import sys
import threading
import time
from typing import List, Union, Dict

print_mutex = threading.Lock()
ip_to_router = dict()


class Node:
    def __init__(self, ip: str, neighbours: List[str], all_ips: List[str]):
        self.ip = ip
        self.lock = threading.Lock()
        self.routing_table = {
            node_ip: {
                'next': node_ip,
                'metric': 1,
            }
            if node_ip in neighbours else
            {
                'next': '0.0.0.0',
                'metric': -1,
            }
            for node_ip in all_ips
            if node_ip != ip
        }

    def print_routing_table(self):
        print('[Source IP]     [Destination IP]        [Next Hop]      [Metric] ')
        for destination_ip, route_attributes in self.routing_table.items():
            print(
                self.ip.ljust(15),
                destination_ip.ljust(23),
                route_attributes['next'].ljust(15),
                str(route_attributes['metric']).rjust(9) if route_attributes['metric'] > 0 else 'inf'.ljust(9),
            )

    def broadcast(self):
        for destination_ip, route_attributes in self.routing_table.items():
            if route_attributes['metric'] != 1:
                continue

            global ip_to_router
            ip_to_router[destination_ip].receive(self.ip, self.routing_table)

    def receive(self, sender_ip: str, received_routing_table: Dict[str, Dict[str, Union[str, int]]]):
        with self.lock:
            for destination_ip, route_attributes in received_routing_table.items():
                if route_attributes['next'] == '0.0.0.0':
                    continue
                if destination_ip == self.ip:
                    continue

                target_metric = route_attributes['metric'] + 1
                if (target_metric < self.routing_table[destination_ip]['metric']
                        or self.routing_table[destination_ip]['metric'] < 0):
                    self.routing_table[destination_ip]['metric'] = target_metric
                    self.routing_table[destination_ip]['next'] = sender_ip

    def simulate(self, sim_cycles):
        global print_mutex
        for sim_step in range(1, sim_cycles + 1):
            with print_mutex:
                print(f'Simulation step {sim_step} of router {self.ip}')
                self.print_routing_table()
                print()
            self.broadcast()
            time.sleep(1)


if __name__ == '__main__':
    simulation_cycles = int(sys.argv[1])

    with open('config.json', 'rt') as graph_file:
        graph = json.load(graph_file)

    ip_addresses = list(graph.keys())

    nodes = [Node(ip, neighbours, ip_addresses) for ip, neighbours in graph.items()]
    ip_to_router = {node.ip: node for node in nodes}

    threads = [threading.Thread(target=node.simulate, args=(simulation_cycles,)) for node in nodes]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    for node in nodes:
        print(f'Final state of router {node.ip} table:')
        node.print_routing_table()
        print()

    print('End of execution!')
