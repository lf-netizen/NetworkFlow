from itertools import chain
from datagram import Datagram
from custom_types import Time
from devices import Router, Endpoint
import timer

class Network:
    def __init__(self, arch) -> None:
        self.routers = {r['id']: Router(r['id'], r['transmission_capacity']) for r in arch['routers']}
        self.endpoints = {e['id']: Endpoint(e['id'], e['gate_id']) for e in arch['endpoints']}
        # iterators
        self.r_it = self.routers.values()
        self.e_it = self.endpoints.values()

    def load_routing_tables(self, routing_tables) -> None:
        for id, rt in routing_tables.items():
            self.routers[id].routing_table = rt

    def load_schedule(self, schedule) -> None:
        for id, sch in schedule.items():
            self.endpoints[id].schedule = [Datagram(id, dg['destination_id'], dg['request_time'], dg['priority']) for dg in sch]
        
        
    def reset_state(self) -> None:
        timer.time = 0
        self.datagrams = []
        for device in chain(self.r_it, self.e_it):
            device.reset()

    def simulate(self, timespan: Time) -> None:
        for _ in range(timespan):
            timer.time += 1
            # send new datagrams to endpoints' gates
            buffer_datagrams = []
            for e in self.endpoints.values():
                buffer_datagrams += e.send_datagrams()
            for id, dgs in buffer_datagrams:
                self.routers[id].receive_datagrams([dgs])
            # send forward datagrams by routers
            buffer_datagrams = []
            for r in self.r_it:
                buffer_datagrams += r.send_datagrams()
            for id, dgs in buffer_datagrams:
                if id in self.routers.keys():
                    self.routers[id].receive_datagrams([dgs])
                else:
                    self.endpoints[id].receive_datagrams([dgs])


if __name__ == '__main__':
    arch = {
        'routers': [
            {'id': 2, 'transmission_capacity':  5}, 
            {'id': 3, 'transmission_capacity': 10}
        ],
        'endpoints': [
            {'id': 1, 'gate_id': 2},
            {'id': 4, 'gate_id': 3},
            {'id': 5, 'gate_id': 3}
        ]
    }
    routing_tables = {
        2: {1: 1, 4: 3, 5: 3},
        3: {1: 2, 4: 4, 5: 5}
    }

    schedule = {
        1: [
            {'destination_id': 4,      'request_time': 1, 'priority': 2},
            {'destination_id': [4, 5], 'request_time': 1, 'priority': 2},
            {'destination_id': 5,      'request_time': 3, 'priority': 1}
        ],
        4: [
            {'destination_id': 1,      'request_time': 1, 'priority': 1}
        ]
    }


    network = Network(arch)
    network.load_schedule(schedule)
    network.load_routing_tables(routing_tables)
    network.simulate(20)
    print('')

