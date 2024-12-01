from sqlmodel import Session

from src.database.entity.denmark_report import DenmarkReportRecord


class DenmarkReportRecordRepository:
    def create(
        self, *, session: Session, report_record: DenmarkReportRecord
    ) -> DenmarkReportRecord:
        session.add(report_record)
        session.commit()
        session.flush(report_record)
        return report_record
