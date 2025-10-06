from collections.abc import Generator
from datetime import datetime

from pydantic import Field

from src.database.entity.denmark_report import DenmarkReportRecord
from src.utils.base_model import BaseModel


class Document(BaseModel):
    document_url: str = Field(alias="dokumentUrl")
    document_mime_type: str = Field(alias="dokumentMimeType")
    document_type: str = Field(alias="dokumentType")


class AccountPeriod(BaseModel):
    start_date: datetime = Field(alias="startDato")
    end_date: datetime = Field(alias="slutDato")


class Approval(BaseModel):
    chair_person: str = Field(alias="dirigent")
    approval_date: datetime = Field(alias="godkendelsesdato")


class FinancialStatement(BaseModel):
    approval: Approval | None = Field(default=None, alias="godkendelse")
    account_period: AccountPeriod = Field(alias="regnskabsperiode")


class Source(BaseModel):
    cvr_number: int | None = Field(alias="cvrNummer")
    registration_number: str | None = Field(default=None, alias="regNummer")
    amendment_reversal: bool = Field(alias="omgoerelse")
    case_number: str = Field(alias="sagsNummer")
    type_of_disclosure: str = Field(alias="offentliggoerelsestype")
    financial_statement: FinancialStatement = Field(alias="regnskab")
    disclosure_time: datetime = Field(alias="offentliggoerelsesTidspunkt")
    import_time: datetime = Field(alias="indlaesningsTidspunkt")
    last_updated: datetime = Field(alias="sidstOpdateret")
    documents: list[Document] = Field(alias="dokumenter")
    import_id: str | None = Field(alias="indlaesningsId")


class Hit(BaseModel):
    index: str = Field(alias="_index")
    type: str = Field(alias="_type")
    id: str = Field(alias="_id")
    score: float = Field(alias="_score")
    source: Source = Field(alias="_source")


class HitsInfo(BaseModel):
    total: int
    max_score: float | None
    hits: list[Hit]


class Shared(BaseModel):
    total: int
    successful: int
    skipped: int
    failed: int


class DenmarkReportApiResponse(BaseModel):
    took: int
    timed_out: bool
    shards: Shared = Field(alias="_shards")
    hits: HitsInfo

    def convert_to_entity(self) -> Generator[DenmarkReportRecord, None, None]:
        for hit in self.hits.hits:
            for doc in hit.source.documents:
                yield DenmarkReportRecord(
                    index_id=hit.id,
                    cvr_number=hit.source.cvr_number,
                    document_mime_type=doc.document_mime_type,
                    document_url=doc.document_url,
                    disclosure_time=hit.source.disclosure_time,
                )
