from queue import Queue
from typing import Any

from src.models.denmark_api import DenmarkReportApiResponse
from src.models.queue_data import QueueData
from src.producer.denmark import DenmarkFinancialReportProducer
from src.utils.constants import ProduceMode, TaskStatus
from src.utils.logger import SystemLogger


class Producer:
    log = SystemLogger.get_logger()

    def __init__(
        self,
        queue: Queue[QueueData[DenmarkReportApiResponse]],
        *,
        produce_mode: ProduceMode,
        **kwargs: Any,
    ) -> None:
        self.queue = queue
        self.produce_mode = produce_mode
        self.denmark_producer = DenmarkFinancialReportProducer()
        self.kwargs = kwargs

    def produce(self, *, time_interval: float = 1.0) -> None:
        match self.produce_mode:
            case ProduceMode.TODAY:
                for response in self.denmark_producer.get_today_reports(
                    time_interval=time_interval
                ):
                    self.log.debug("[Producer] Put the message to the queue")
                    self.queue.put(
                        QueueData(data=response, task_status=TaskStatus.IN_PROGRESS)
                    )
                self.queue.put(QueueData(data=None, task_status=TaskStatus.FINISHED))

            case ProduceMode.DATE_RANGE:
                start_date, end_date = (
                    self.kwargs["start_date"],
                    self.kwargs["end_date"],
                )
                for response in self.denmark_producer.get_date_range_reports(
                    start_date=start_date,
                    end_date=end_date,
                    time_interval=time_interval,
                ):
                    self.log.debug("[Producer] Put the message to the queue")
                    self.queue.put(
                        QueueData(data=response, task_status=TaskStatus.IN_PROGRESS)
                    )
                self.queue.put(QueueData(data=None, task_status=TaskStatus.FINISHED))

            case _:
                raise ValueError("Invalid produce mode")
