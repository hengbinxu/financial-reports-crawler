from pydantic import BaseModel as _BaseModel
from pydantic.config import ConfigDict


class BaseModel(_BaseModel):
    model_config = ConfigDict(populate_by_name=True)
