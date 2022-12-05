from custom_types import Time

class Datagram:
    def __init__(self, source_id: int, destination_id: int, request_time: Time) -> None:
        self.source_id = source_id
        self.destination_id = destination_id
        self.request_time = request_time
        