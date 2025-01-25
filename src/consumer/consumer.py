from queue import Queue

from src.consumer.denmark import DenmarkFinancialReportConsumer
from src.models.denmark_api import DenmarkReportApiResponse
from src.models.queue_data import QueueData
from src.utils.constants import TaskStatus
from src.utils.logger import SystemLogger


class Consumer:
    log = SystemLogger.get_logger()

    def __init__(self, queue: Queue[QueueData[DenmarkReportApiResponse]]) -> None:
        self.queue = queue
        self.denmark_consumer = DenmarkFinancialReportConsumer()

    def consume(self) -> None:
        self.log.debug("[Consumer] Start consuming the queue")
        while True:
            queue_data = self.queue.get()
            match queue_data.task_status:
                case TaskStatus.IN_PROGRESS:
                    self.log.debug("[Consumer] Get the data from the queue")
                    self.denmark_consumer.download_report(queue_data.data)

                case TaskStatus.FINISHED:
                    self.log.debug("[Consumer] Stop consuming the queue")
                    break

                case _:
                    raise ValueError(f"Invalid task status: {queue_data.task_status}")
