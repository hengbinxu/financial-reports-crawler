from http import HTTPMethod
from pathlib import Path

from sqlalchemy.exc import IntegrityError

from src.database.client import sql_connector
from src.database.entity import DenmarkReportRecord
from src.database.repository import DenmarkReportRecordRepository
from src.google_api.denmark_data_storage import DenmarkDataStorage
from src.models.denmark_api import DenmarkReportApiResponse
from src.utils.logger import SystemLogger
from src.utils.type_alias import StrPath
from src.utils.utils import HelperFunc


class DenmarkFinancialReportConsumer:
    log = SystemLogger.get_logger()
    _DOWNLOAD_PATH = HelperFunc.get_root_dir() / "downloads"

    def __init__(self) -> None:
        self._DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
        self.denmark_report_record_repo = DenmarkReportRecordRepository()
        self.denmark_data_storage = DenmarkDataStorage()

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
            self.upload_to_google_drive(output_path)

    def upload_to_google_drive(self, file_path: StrPath) -> None:
        """
        Upload file to Google Drive

        Args:
            file_path (StrPath)
        """
        # Ex: 2025-01/xml/35040862-2025-01-25-urn:ofk:oid:36899396.xml
        relative_path = file_path.relative_to(self._DOWNLOAD_PATH)
        year_month, file_extension, _ = str(relative_path).split("/")
        year_month_dir_drive_id = (
            self.denmark_data_storage.find_root_path_folder_id_by_name(year_month)
        )
        if year_month_dir_drive_id is None:
            create_res = self.denmark_data_storage.create_folder_on_root(year_month)
            year_month_dir_drive_id = create_res.id

        # Get file extension directory
        file_extension_dir_drive_id = self.denmark_data_storage.find_folder_id_by_name(
            folder_name=file_extension, drive_id=year_month_dir_drive_id
        )
        if file_extension_dir_drive_id is None:
            create_res = self.denmark_data_storage.create_folder(
                name=file_extension, parent_drive_ids=[year_month_dir_drive_id]
            )
            file_extension_dir_drive_id = create_res.id

        # Upload file
        self.denmark_data_storage.upload_file(
            file_path=file_path, parent_drive_ids=[file_extension_dir_drive_id]
        )
        self.log.debug(f"[Consumer] Successfully uploaded file: {file_path}")

    def _write_to_db(self, report_record: DenmarkReportRecord) -> None:
        with sql_connector.start_session() as session:
            self.denmark_report_record_repo.create(
                session=session, report_record=report_record
            )
        self.log.debug(
            f"[Consumer] Successfully added record to database: {report_record}"
        )
