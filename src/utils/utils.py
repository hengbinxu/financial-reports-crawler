import hashlib
import json
import pickle
from datetime import datetime, timedelta, timezone
from http import HTTPMethod
from pathlib import Path
from typing import Any, Generator, List

from httpx import Client

from src.utils.logger import SystemLogger
from src.utils.type_alias import StrPath

from .. import ROOT_DIR

log = SystemLogger.get_logger()


class HelperFunc:
    @staticmethod
    def get_root_dir() -> Path:
        return ROOT_DIR

    @staticmethod
    def download_file(
        http_method: HTTPMethod = HTTPMethod.GET,
        *,
        url: str,
        output_path: StrPath,
        chunk_size: int = 1024,
        **kwargs: Any,
    ) -> None:
        client = Client()
        with client.stream(http_method, url, **kwargs) as response:
            with open(output_path, "wb") as wf:
                for chunk in response.iter_bytes(chunk_size=chunk_size):
                    wf.write(chunk)
        log.debug(f"Downloaded url: {url} file to {output_path}")

    @staticmethod
    def get_now() -> datetime:
        return datetime.now(tz=timezone.utc)

    @staticmethod
    def get_range_dates(
        *, start_date: datetime, end_date: datetime
    ) -> Generator[datetime, None, None]:
        while start_date < end_date:
            yield start_date
            start_date += timedelta(days=1)

    @staticmethod
    def read_json(path: StrPath) -> Any:
        with open(path) as rf:
            data = json.load(rf)
        return data

    @staticmethod
    def write_json(*, path: StrPath, data: Any) -> None:
        with open(path, "w") as wf:
            json.dump(data, wf, ensure_ascii=False)
        log.debug(f"Write data to {path}")

    @staticmethod
    def write_file(*, path: StrPath, data: Any) -> None:
        with open(path, "w") as wf:
            wf.write(data)
        log.debug(f"Write data to {path}")

    @staticmethod
    def hash_list(data: List[Any]) -> str:
        return hashlib.sha256(pickle.dumps(data)).hexdigest()
