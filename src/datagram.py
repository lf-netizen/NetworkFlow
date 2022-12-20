from custom_types import Time, ID
from dataclasses import dataclass, field

@dataclass
class Datagram:
    source_id: ID
    destination_id: ID | list[ID]
    request_time: Time
    priority: int
    arrival_time: Time = None
    to_termination: int = 20
    route: list[ID] = field(default_factory=list)

    def __lt__(self, other):
        return self.priority <  other.priority if self.priority != other.priority else  self.request_time <  other.request_time
    def  __le__(self, other):
        return self.priority <= other.priority if self.priority != other.priority else  self.request_time <= other.request_time
    def  __gt__(self, other):
        return self.priority >  other.priority if self.priority != other.priority else  self.request_time >  other.request_time
    def  __ge__(self, other):
        return self.priority >= other.priority if self.priority != other.priority else  self.request_time >= other.request_time
        
class TerminationError(Exception):
        pass

if __name__ == '__main__':
    d1 = Datagram(1, 1, 10, 1)
    d2 = Datagram(3, 1, 10, 2)
    d3 = Datagram(4, 1, 11, 2)
    d4 = Datagram(2, 1, 11, 1)

    from queue import PriorityQueue
    q = PriorityQueue()
    for item in [d1, d2, d3, d4]:
        q.put(item)

    while not q.empty():
        print(q.get())
    