from itertools import chain
from custom_types import Time, ID
from devices import Router, Endpoint, IDevice
from datagram import Datagram, TerminationError
import timer
import copy
testval = 1000
global_logs = {}

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

        self.logs = {'edges_weight': {d.id: {} for d in chain(self.r_it, self.e_it)}, 
                     'queue_status': {r.id: [] for r in self.r_it}
                    }

    def load_routing_tables(self, routing_tables) -> None:
        for id, rt in routing_tables.items():
            self.routers[id].routing_table = rt

    def load_schedule(self, schedule) -> None:
        self.schedule = schedule
        for id, sch in schedule.items():
            self.endpoints[id].schedule = [Datagram(id, dg['destination_id'], dg['request_time'], 
                                                    dg['priority'], to_termination=len(self.routers)+1, route=[id]) for dg in sch]
        
    @staticmethod
    def reset_devices_ids():
        IDevice.endpoints_ids = set()
        IDevice.routers_ids = set()
    
    def reset_state(self, with_schedule: bool = True, with_devices: bool = False) -> None:
        timer.time = 0
        self.datagrams = []
        self.logs = {'edges_weight': {d.id: {} for d in chain(self.r_it, self.e_it)}, 
                     'queue_status': {r.id: [] for r in self.r_it}
                    }
        for device in chain(self.r_it, self.e_it):
            device.reset()
        if not with_schedule:
            self.load_schedule(self.schedule)
        if with_devices:
            self.routers = {}
            self.endpoints = {}
            IDevice.endpoints_ids = set()
            IDevice.routers_ids = set()

    def simulate(self, ticks: Time = None) -> float:
        if self.schedule is None:
            raise ValueError('Schedule is empty')

        total_datagrams = sum([1 if isinstance(dg['destination_id'], ID) else len(dg['destination_id']) for sch in self.schedule.values() for dg in sch])
        if total_datagrams == 0:
            raise ValueError('Schedule contains no datagrams to be sent')

        # calculate current state of the simulation
        datagrams_to_be_sent = sum([1 if isinstance(dg.destination_id, ID) else len(dg.destination_id) for e in self.endpoints.values() for dg in e.schedule])
        datagrams_in_network = sum([len(r.queue.queue) for r in self.routers.values()])
        received_datagrams = sum([len(e.received_datagrams) for e in self.endpoints.values()])
        terminated_datagrams = total_datagrams - received_datagrams - datagrams_in_network - datagrams_to_be_sent

        init_time = timer.time
        under_time_limit = lambda: True if ticks is None else timer.time < init_time + ticks
        not_finished = lambda: total_datagrams > terminated_datagrams + received_datagrams
        run_simulation = lambda: under_time_limit() and not_finished()

        while run_simulation():
            timer.time += 1
            if timer.time > 10e4:
                raise TimeoutError('Infinite simulation. You may try to reset state before calling simulate.')
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
                    received_datagrams += 1

            # logging router queue status
            for r in self.r_it:
                self.logs['queue_status'][r.id].append(len(r.queue.queue))

        # calculate loss function
        total_time = 0
        for e in self.e_it:
            for dg in e.received_datagrams:
                total_time += dg.arrival_time - dg.request_time
        avg_time = 0 if received_datagrams == 0 else total_time / received_datagrams
        loss = avg_time + 0.2 * terminated_datagrams

        # create logs
        # count how many datagrams went through an edge
        for e in self.e_it:
            for dg in e.received_datagrams:
                for src, dst in zip(dg.route[:-1], dg.route[1:]):
                    if dst not in self.logs['edges_weight'][src]:
                        self.logs['edges_weight'][src][dst] = 0
                    self.logs['edges_weight'][src][dst] += 1

        return loss


if __name__ == '__main__':
    arch = {
        'routers': [
            {'id': 0, 'transmission_capacity': 3},
            {'id': 1, 'transmission_capacity': 3},
            {'id': 2, 'transmission_capacity': 3},
            {'id': 3, 'transmission_capacity': 3},
        ],
        'endpoints': [
            {'id': 4, 'gate_id': 0},
            {'id': 5, 'gate_id': 1},
            {'id': 6, 'gate_id': 2},
            {'id': 7, 'gate_id': 3}
        ]
    }
    schedule = {
        4: [
            {'destination_id': 5, 'request_time': 1, 'priority': 1},
            {'destination_id': 6, 'request_time': 1, 'priority': 1},
            {'destination_id': 7, 'request_time': 1, 'priority': 1}
        ],
        5: [
            {'destination_id': 4, 'request_time': 1, 'priority': 1},
            {'destination_id': 6, 'request_time': 1, 'priority': 1},
            {'destination_id': 7, 'request_time': 1, 'priority': 1}
        ],
        6: [
            {'destination_id': 4, 'request_time': 1, 'priority': 1},
            {'destination_id': 5, 'request_time': 1, 'priority': 1},
            {'destination_id': 7, 'request_time': 1, 'priority': 1}
        ],
        7: [
            {'destination_id': 4, 'request_time': 1, 'priority': 1},
            {'destination_id': 5, 'request_time': 1, 'priority': 1},
            {'destination_id': 6, 'request_time': 1, 'priority': 1}
        ]
    }
    # routing_tables = {
    #     0: {4: 4, 5: 1, 6: 2, 7: 2},
    #     1: {5: 5, 6: 2, 7: 2, 4: 0},
    #     2: {6: 6, 7: 3, 4: 1, 5: 1},
    #     3: {6: 0, 7: 7, 4: 1, 5: 0}
    #     }

    routing_tables = {0: {4: 4, 5: 3, 6: 2, 7: 2}, 1: {5: 5, 6: 0, 7: 3, 4: 0}, 2: {6: 6, 7: 3, 4: 0, 5: 1}, 3: {7: 7, 4: 0, 5: 2, 6: 1}}
    # example pipeline
    network = Network(arch)
    network.load_schedule(schedule)
    for _ in range(50):
        network.load_routing_tables(routing_tables)  # assuming routing tables are modified with every iteration
        loss = network.simulate()
        network.reset_state(with_schedule=False)
        print(loss)

