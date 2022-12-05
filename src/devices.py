from abc import ABC, abstractmethod
import itertools
from queue import PriorityQueue


class IDevice(ABC):
    new_id = itertools.count().next
    def __init__(self) -> None:
        super().__init__()
        self.id = IDevice.new_id()


    @abstractmethod
    def send_messages(self) -> list[int]:
        pass
    
class Router(IDevice):
    def __init__(self, speed: int, neighbour_ids: list[int]) -> None:
        super().__init__()
        self.speed = speed # number of datagrams sent per time unit
        self.neighbour_ids = []
        self.queue = PriorityQueue()
        