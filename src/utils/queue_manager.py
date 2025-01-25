from queue import Queue

from src.models.queue_data import QueueData


class QueueManager[T]:
    def __init__(self, max_size: int = 10) -> None:
        self.queue: Queue[QueueData[T]] = Queue[QueueData[T]](max_size)

    def get_queue(self) -> Queue[QueueData[T]]:
        return self.queue
