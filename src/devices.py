from abc import ABC, abstractmethod
from queue import PriorityQueue
from datagram import Datagram
from custom_types import Time, ID

timer: Time = 0

class IDevice(ABC):
    routers_ids = set()
    endpoints_ids = set()
    def __init__(self, id: ID) -> None:
        super().__init__()
        if id in self.routers_ids.union(self.endpoints_ids):
            raise ValueError(f"duplicate id: {id}")
        self.id = id

    @abstractmethod
    def send_datagram(self) -> list[tuple[ID, Datagram]]:
        pass

    @abstractmethod
    def receive_datagram(self, datagrams: list[Datagram]) -> None:
        pass
    
class Router(IDevice):
    def __init__(self, id: ID, transmission_capacity: int, neighbour_ids: list[ID], routing_table: dict[ID: ID]) -> None:
        super().__init__(id)
        self.routers_ids.add(id)

        self.transmission_capacity = transmission_capacity # number of datagrams sent per time unit
        self.neighbour_ids = neighbour_ids
        self.routing_table = routing_table
        self.queue = PriorityQueue[Datagram]()

    def send_datagram(self) -> list[tuple[ID, Datagram]]:
        data_to_be_sent = []
        for _ in range(self.transmission_capacity):
            if self.queue.empty():
                break
            else:
                dg = self.queue.get()
                if dg.destination_id not in self.routing_table:
                    raise LookupError(f"destination id {dg.destination_id} not in routing table of router {self.id}")
                next_id = self.routing_table[dg.destination_id]
                data_to_be_sent.append((next_id, dg))
        
        return data_to_be_sent

    def receive_datagram(self, datagrams: list[Datagram]) -> None:
        for dg in datagrams:
            self.queue.put(dg)

class Endpoint(IDevice):
    def __init__(self, id: ID, gate_id: ID, schedule: list[Datagram]) -> None:
        super().__init__(id)
        self.endpoints_ids.add(id)
        self.gate_id = gate_id
        self.schedule = sorted(schedule, key=lambda dg: dg.request_time)
        self.received_datagrams: list[Datagram] = []

    def send_datagram(self) -> list[tuple[ID, Datagram]]:
        if not self.schedule:
            return
        data_to_be_sent = []
        while self.schedule[0].request_time == timer:
            data_to_be_sent.append(self.schedule.pop(0))
        data_to_be_sent = [(self.gate_id, dg) for dg in self.schedule[timer]]
        return data_to_be_sent

    def receive_datagram(self, datagrams: list[Datagram]) -> None:
        for dg in datagrams:
            dg.arrival_time = timer
        self.received_datagrams += datagrams


if __name__ == '__main__':
    r1 = Router(id=1, transmission_capacity=1, neighbour_ids=[2], routing_table={2: 2})
    r2 = Router(id=2, transmission_capacity=10, neighbour_ids=[1], routing_table={1: 1})

    dg1 = Datagram(1, 2, 1, 1)
    dg2 = Datagram(1, 2, 1, 2)
    dg3 = Datagram(1, 2, 4, 2)
    print('')

    