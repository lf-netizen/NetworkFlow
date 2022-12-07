import sys
import copy
from abc import ABC, abstractmethod
from queue import PriorityQueue
from datagram import Datagram, TerminationError
from custom_types import ID
import timer

class IDevice(ABC):
    routers_ids = set()
    endpoints_ids = set()
    def __init__(self, id: ID) -> None:
        super().__init__()
        if id in self.routers_ids.union(self.endpoints_ids):
            raise ValueError(f"Duplicate id: {id}.")
        self.id = id

    @abstractmethod
    def send_datagrams(self) -> list[tuple[ID, Datagram]]:
        pass

    @abstractmethod
    def receive_datagram(self, dg: Datagram) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass
    

class Router(IDevice):
    def __init__(self, id: ID, transmission_capacity: int, routing_table: dict[ID: ID] = {}) -> None:
        super().__init__(id)
        self.routers_ids.add(id)

        self.transmission_capacity = transmission_capacity # number of datagrams sent per time unit
        self.routing_table = routing_table
        self.queue: PriorityQueue[Datagram] = PriorityQueue()
        
    @property
    def routing_table(self) -> dict[ID: ID]:
        return self._routing_table

    @routing_table.setter
    def routing_table(self, rt: dict[ID: ID]) -> None:
        adresses = set(rt.keys())
        if adresses != self.endpoints_ids:
            raise ValueError(f'Router {self.id}: missing/extra endpoints in routing table.')
        self._routing_table = rt

    def send_datagrams(self) -> list[tuple[ID, Datagram]]:
        data_to_be_sent = []
        for _ in range(self.transmission_capacity):
            if self.queue.empty():
                break
            dg = self.queue.get()
            
            dest_id = dg.destination_id if isinstance(dg.destination_id, int) else dg.destination_id[0]
            next_id = self.routing_table[dest_id]
            data_to_be_sent.append((next_id, dg))
        
        return data_to_be_sent

    def receive_datagram(self, dg: Datagram) -> None:
        dg.to_termination -= 1
        if not dg.to_termination:
            raise TerminationError()

        dest_id = dg.destination_id
        # single receiver
        if isinstance(dest_id, int):
            if dest_id not in self.routing_table:
                raise KeyError(f"Destination id {dg.destination_id} not in routing table of router {self.id}.")
            self.queue.put(dg)
            return
        # multiple receivers
        try:
            next_id = [self.routing_table[id] for id in dest_id]
        except KeyError as e:
            print(e)
            print(f'The routing table of router {self.id} is incomplete. Terminating the program...')
            sys.exit()
        
        unique_next = set(next_id)
        for u_n in unique_next:
            split_dg = copy.copy(dg)
            split_dest_id = [dest_id[i] for i in [i for i, id in enumerate(next_id) if id == u_n]]
            if len(split_dest_id) == 1:
                split_dest_id = split_dest_id[0]
            split_dg.destination_id = split_dest_id
            self.queue.put(split_dg)
                
    def reset(self) -> None:
        self.queue = PriorityQueue()

class Endpoint(IDevice):
    def __init__(self, id: ID, gate_id: ID, schedule: list[Datagram] = []) -> None:
        super().__init__(id)
        self.endpoints_ids.add(id)

        self.gate_id = gate_id
        self.schedule = sorted(schedule, key=lambda dg: dg.request_time)
        self.received_datagrams: list[Datagram] = []

    def send_datagrams(self) -> list[tuple[ID, Datagram]]:
        if not self.schedule:
            return []
        data_to_be_sent = []
        while len(self.schedule) and self.schedule[0].request_time == timer.time:
            data_to_be_sent.append((self.gate_id, self.schedule.pop(0)))
        return data_to_be_sent

    def receive_datagram(self, dg: Datagram) -> None:
        dg.arrival_time = timer.time
        self.received_datagrams.append(dg)

    def reset(self) -> None:
        self.schedule = []
        self.received_datagrams = []


if __name__ == '__main__':
    dg1 = Datagram(1, 4, 1, 2)
    dg2 = Datagram(1, [4, 5], 1, 1)
    dg3 = Datagram(1, 4, 5, 1)
    dg4 = Datagram(1, [5], 6, 1)

    e1 = Endpoint(id=1, gate_id=2, schedule=[dg1, dg2, dg3, dg4])
    e2 = Endpoint(id=4, gate_id=3)
    e3 = Endpoint(id=5, gate_id=3)
    r1 = Router(id=2, transmission_capacity=1,  routing_table={4: 3, 5: 3})
    r2 = Router(id=3, transmission_capacity=10, routing_table={4: 4, 5: 5})


    timer.time += 1
    for _, dg in e1.send_datagrams():
        r1.receive_datagram(dg)
    for _, dg in r1.send_datagrams():
        r2.receive_datagram(dg)
    print('')

    