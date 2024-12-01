from datetime import datetime

import click
from click.core import Context, Option

from src.consumer.consumer import Consumer
from src.database.client import sql_connector
from src.models.denmark_api import DenmarkReportApiResponse
from src.producer.producer import Producer
from src.utils.constants import ProduceMode
from src.utils.queue_manager import QueueManager


class ProduceModeType(click.ParamType):
    name = "produce_mode"

    def convert(self, value: str, param: Option, ctx: Context) -> ProduceMode | None:
        match value:
            case "today":
                return ProduceMode.TODAY
            case "date_range":
                return ProduceMode.DATE_RANGE
            case _:
                self.fail(f"Invalid produce mode: {value}", param, ctx)
                return None


@click.command()
@click.option(
    "--produce-mode",
    "-pm",
    "produce_mode",
    type=ProduceModeType(),
    required=True,
    help="Produce mode [today, date_range]",
)
@click.option(
    "--start-date",
    "-sd",
    "start_date",
    type=click.DateTime(),
    default=None,
    help="Start date for the report",
)
@click.option(
    "--end-date",
    "-ed",
    "end_date",
    type=click.DateTime(),
    default=None,
    help="End date for the report",
)
def main(
    produce_mode: ProduceMode,
    start_date: datetime | None,
    end_date: datetime | None,
) -> None:
    sql_connector.init_db()
    queue_manager = QueueManager[DenmarkReportApiResponse]()
    queue = queue_manager.get_queue()
    producer = Producer(
        queue,
        produce_mode=produce_mode,
        start_date=start_date,
        end_date=end_date,
    )
    consumer = Consumer(queue)

    producer.produce()
    consumer.consume()


if __name__ == "__main__":
    main()
