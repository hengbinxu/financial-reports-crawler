from http import HTTPMethod
from pathlib import Path

from sqlalchemy.exc import IntegrityError

from src.database.client import sql_connector
from src.database.entity import DenmarkReportRecord
from src.database.repository import DenmarkReportRecordRepository
from src.models.denmark_api import DenmarkReportApiResponse
from src.utils.logger import SystemLogger
from src.utils.utils import HelperFunc


class DenmarkFinancialReportConsumer:
    log = SystemLogger.get_logger()
    _DOWNLOAD_PATH = HelperFunc.get_root_dir() / "downloads"

    def __init__(self) -> None:
        self._DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
        self.denmark_report_record_repo = DenmarkReportRecordRepository()

    def _get_output_file_path(self, report_dao: DenmarkReportRecord) -> Path:
        year, month, _ = report_dao.get_disclosure_info()
        ext = report_dao.get_file_extension()
        output_dir = self._DOWNLOAD_PATH / f"{year}-{month:02}" / ext
        if output_dir.exists() is False:
            output_dir.mkdir(parents=True, exist_ok=True)
        file_name = report_dao.get_file_name()
        return output_dir / file_name

    def download_report(self, report_response: DenmarkReportApiResponse) -> None:
        for report_info in report_response.convert_to_entity():
            try:
                self._write_to_db(report_info)
            except IntegrityError:
                self.log.debug(f"[Consumer] Record already exists: {report_info}")
                continue

            output_path = self._get_output_file_path(report_info)
            HelperFunc.download_file(
                HTTPMethod.GET, url=report_info.document_url, output_path=output_path
            )

    def _write_to_db(self, report_record: DenmarkReportRecord) -> None:
        with sql_connector.start_session() as session:
            self.denmark_report_record_repo.create(
                session=session, report_record=report_record
            )
        self.log.debug(
            f"[Consumer] Successfully added record to database: {report_record}"
        )
