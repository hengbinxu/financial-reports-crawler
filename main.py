import random
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime
from typing import Any

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
    queue_manager = QueueManager[DenmarkReportApiResponse](max_size=60)
    queue = queue_manager.get_queue()
    producer = Producer(
        queue,
        produce_mode=produce_mode,
        start_date=start_date,
        end_date=end_date,
    )
    consumer = Consumer(queue)

    tasks_args: list[dict[str, Any]] = [
        {
            "fn": producer.produce,
            "kwargs": {"time_interval": random.uniform(0.5, 3.0)},
        },
        # Can add more consumer here
        {"fn": consumer.consume, "kwargs": {}},
    ]
    with ThreadPoolExecutor(max_workers=2) as executor:
        tasks: list[Future[Any]] = []
        for task_args in tasks_args:
            if task_args["kwargs"]:
                tasks.append(executor.submit(task_args["fn"], **task_args["kwargs"]))
            else:
                tasks.append(executor.submit(task_args["fn"]))

    for task in tasks:
        task.result()


if __name__ == "__main__":
    main()

# TODO:
# 1. Improve the threading stopping mechanism
# 2. Add Dockerfile
# 3. Change package management from property to uv
# 4. Add thread locking mechanism
# 5. Deploy onto github actions
