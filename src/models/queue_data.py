from pydantic import Field

from src.utils.base_model import BaseModel
from src.utils.constants import TaskStatus


class QueueData[T](BaseModel):
    data: T | None = Field(default=None)
    task_status: TaskStatus
