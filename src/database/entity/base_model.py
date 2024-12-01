from datetime import datetime

from sqlmodel import Field, SQLModel

from src.utils.utils import HelperFunc


class BaseModel(SQLModel):
    pass


class BasePrimaryKeyModel(BaseModel):
    id: int | None = Field(default=None, primary_key=True)
    created_time: datetime = Field(default_factory=HelperFunc.get_now, nullable=False)
