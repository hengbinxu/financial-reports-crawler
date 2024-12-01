import math
from datetime import datetime, timedelta
from typing import Any, Dict, Generator

from src.models.denmark_api import DenmarkReportApiResponse
from src.utils.base_client import BaseClient
from src.utils.base_router import Router, UrlPath
from src.utils.config import settings
from src.utils.headers import json_headers
from src.utils.utils import HelperFunc

__all__ = ["DenmarkFinancialReportProducer"]

_denmark_router = Router(
    [
        UrlPath(name="denmark_report", path=settings.DENMARK_REPORT_URL),
        UrlPath(name="denmark_cvr_number", path=settings.DENMARK_CVR_API_ULR),
    ]
)


class DenmarkFinancialReportProducer(BaseClient):
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    PAGE_SIZE = 100

    def __init__(self) -> None:
        super().__init__(url_router=_denmark_router)
        self.headers = json_headers

    @classmethod
    def _get_query(
        cls, start_date: str, end_date: str, page: int, page_size: int
    ) -> Dict[str, Any]:
        return {
            "query": {
                "bool": {
                    "must": [
                        # {"term": {"dokumenter.dokumentMimeType": "application"}},
                        # {"term": {"dokumenter.dokumentMimeType": "xml"}},
                        {
                            "range": {
                                # Disclosure Time/Publication Time
                                "offentliggoerelsesTidspunkt": {
                                    "gt": start_date,
                                    "lt": end_date,
                                }
                            }
                        },
                    ],
                    "must_not": [],
                    "should": [],
                }
            },
            "size": page_size,
            "from": page,
        }

    @classmethod
    def _date_to_str(cls, date_time: datetime) -> str:
        return date_time.strftime(cls.DATE_FORMAT)

    def _request_report(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
        page: int = 1,
    ) -> DenmarkReportApiResponse:
        start_date_str = self._date_to_str(start_date)
        end_date_str = self._date_to_str(end_date)
        res = self.post(
            api_name="denmark_report",
            json=self._get_query(start_date_str, end_date_str, page, self.PAGE_SIZE),
            headers=self.headers,
        )
        return DenmarkReportApiResponse(**res.json())

    def get_date_range_reports(
        self, start_date: datetime, end_date: datetime
    ) -> Generator[DenmarkReportApiResponse, None, None]:
        response = self._request_report(start_date=start_date, end_date=end_date)
        self.log.debug(f"Total hits: {response.hits.total}")
        yield response
        required_request_times = math.ceil(response.hits.total / self.PAGE_SIZE)
        if required_request_times <= 0:
            return

        for page in range(1, required_request_times):
            response = self._request_report(
                start_date=start_date, end_date=end_date, page=page
            )
            yield response

    def get_today_reports(self) -> Generator[DenmarkReportApiResponse, None, None]:
        date_format = "%Y-%m-%d"
        today = datetime.strptime(
            HelperFunc.get_now().strftime(date_format), date_format
        )
        tomorrow = today + timedelta(days=1)
        yield from self.get_date_range_reports(today, tomorrow)
