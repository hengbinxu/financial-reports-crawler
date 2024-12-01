from queue import Queue


class QueueManager[T]:
    def __init__(self, max_size: int = 10) -> None:
        self.queue: Queue[T] = Queue[T](max_size)

    def get_queue(self) -> Queue[T]:
        return self.queue
