from queue import Queue
from typing import Any

from src.models.denmark_api import DenmarkReportApiResponse
from src.producer.denmark import DenmarkFinancialReportProducer
from src.utils.constants import ProduceMode
from src.utils.logger import SystemLogger


class Producer:
    log = SystemLogger.get_logger()

    def __init__(
        self,
        queue: Queue[DenmarkReportApiResponse],
        *,
        produce_mode: ProduceMode,
        **kwargs: Any,
    ) -> None:
        self.queue = queue
        self.produce_mode = produce_mode
        self.denmark_producer = DenmarkFinancialReportProducer()
        self.kwargs = kwargs

    def produce(self) -> None:
        match self.produce_mode:
            case ProduceMode.TODAY:
                for response in self.denmark_producer.get_today_reports():
                    self.log.debug("[Producer] Put the message to the queue")
                    self.queue.put(response)

            case ProduceMode.DATE_RANGE:
                start_date, end_date = (
                    self.kwargs["start_date"],
                    self.kwargs["end_date"],
                )
                for response in self.denmark_producer.get_date_range_reports(
                    start_date=start_date, end_date=end_date
                ):
                    self.log.debug("[Producer] Put the message to the queue")
                    self.queue.put(response)

            case _:
                raise ValueError("Invalid produce mode")
