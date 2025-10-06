from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from sqlmodel import Session, SQLModel, create_engine

from src.config import settings
from src.utils.constants import Envs
from src.utils.logger import SystemLogger


class SqlConnector:
    log = SystemLogger.get_logger()

    def __init__(self, db_url: str = settings.DB_URL) -> None:
        self.db_url = db_url
        self.engine = create_engine(
            self.db_url, echo=True if settings.ENV == Envs.DEV else False
        )

    @contextmanager
    def start_session(
        self, *args: Any, **kwargs: Any
    ) -> Generator[Session, None, None]:
        with Session(self.engine, *args, **kwargs) as session:
            try:
                yield session
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()

    def init_db(self) -> None:
        SQLModel.metadata.create_all(self.engine)
        self.log.debug("Successfully created database tables")


sql_connector = SqlConnector()
