from queue import Queue

from src.consumer.denmark import DenmarkFinancialReportConsumer
from src.models.denmark_api import DenmarkReportApiResponse
from src.utils.logger import SystemLogger


class Consumer:
    log = SystemLogger.get_logger()

    def __init__(self, queue: Queue[DenmarkReportApiResponse]) -> None:
        self.queue = queue
        self.denmark_consumer = DenmarkFinancialReportConsumer()

    def consume(self) -> None:
        response: DenmarkReportApiResponse
        while not self.queue.empty():
            response = self.queue.get()
            self.log.debug("[Consumer] Get the message from the queue")
            self.denmark_consumer.download_report(response)
