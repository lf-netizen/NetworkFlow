from itertools import chain
from custom_types import Time
from devices import Router, Endpoint
from datagram import Datagram, TerminationError
import timer

class Network:
    def __init__(self, arch) -> None:
        self.routers   = {r['id']: Router(r['id'], r['transmission_capacity']) 
                                                        for r in arch['routers']}
        self.endpoints = {e['id']: Endpoint(e['id'], e['gate_id']) 
                                                        for e in arch['endpoints']}
        self.schedule = None
        # iterators
        self.r_it = self.routers.values()
        self.e_it = self.endpoints.values()

    def load_routing_tables(self, routing_tables) -> None:
        for id, rt in routing_tables.items():
            self.routers[id].routing_table = rt

    def load_schedule(self, schedule) -> None:
        self.schedule = schedule
        for id, sch in schedule.items():
            self.endpoints[id].schedule = [Datagram(id, dg['destination_id'], dg['request_time'], 
                                                    dg['priority'], to_termination=len(self.routers)+1) for dg in sch]
        
        
    def reset_state(self, with_schedule: bool = True) -> None:
        timer.time = 0
        self.datagrams = []
        for device in chain(self.r_it, self.e_it):
            device.reset()
        if not with_schedule:
            self.load_schedule(self.schedule)

    def simulate(self, timespan: Time) -> float:
        terminated_datagrams = 0
        for _ in range(timespan):
            timer.time += 1
            # send new datagrams to endpoints' gates
            buffer_datagrams = []
            for e in self.e_it:
                buffer_datagrams += e.send_datagrams()
            for id, dg in buffer_datagrams:
                try:
                    self.routers[id].receive_datagram(dg)
                except TerminationError as e:
                    terminated_datagrams += 1
            # send forward datagrams by routers
            buffer_datagrams = []
            for r in self.r_it:
                buffer_datagrams += r.send_datagrams()
            for id, dg in buffer_datagrams:
                if id in self.routers.keys():
                    try:
                        self.routers[id].receive_datagram(dg)
                    except TerminationError as e:
                        terminated_datagrams += 1
                else:
                    self.endpoints[id].receive_datagram(dg)

        # calculate loss function
        # punishment for lost datagrams
        total_time = timespan * terminated_datagrams
        total_datagrams = terminated_datagrams
        for e in self.e_it:
            total_datagrams += len(e.received_datagrams)
            for dg in e.received_datagrams:
                total_time += dg.arrival_time - dg.request_time
        
        if total_datagrams == 0:
            raise ValueError('Schedule contains no datagrams to be sent within simulation timespan')

        loss = total_time / total_datagrams
        return loss


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

    # example pipeline
    network = Network(arch)
    network.load_schedule(schedule)
    for _ in range(2):
        network.load_routing_tables(routing_tables) # assuming routing tables are modified with every iteration
        loss = network.simulate(20)
        network.reset_state(with_schedule=False)
        print(loss)

