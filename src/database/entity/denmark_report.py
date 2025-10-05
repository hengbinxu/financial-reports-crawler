import os
from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from src.database.entity.base_model import BasePrimaryKeyModel


class DenmarkReportRecord(BasePrimaryKeyModel, table=True):  # type: ignore
    __tablename__: str = "denmark_report_record"
    __table_args__ = (UniqueConstraint("index_id", "document_url"),)

    index_id: str = Field(index=True, nullable=False)
    cvr_number: int | None = Field(default=None, index=True)
    document_url: str = Field(unique=True, nullable=False)
    document_mime_type: str = Field(nullable=False)
    disclosure_time: datetime = Field(nullable=False)

    def get_disclosure_info(self) -> tuple[int, int, int]:
        return (
            self.disclosure_time.year,
            self.disclosure_time.month,
            self.disclosure_time.day,
        )

    def get_file_extension(self) -> str:
        _, ext = os.path.splitext(self.document_url)
        return ext.replace(".", "")

    def get_file_name(self) -> str:
        year, month, day = self.get_disclosure_info()
        ext = self.get_file_extension()
        if self.cvr_number is None:
            return f"unknown-{year}-{month:02}-{day:02}-{self.index_id}.{ext}"
        return f"{self.cvr_number}-{year}-{month:02}-{day:02}-{self.index_id}.{ext}"
