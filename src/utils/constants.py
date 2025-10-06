from enum import Enum

from src import ROOT_DIR

COOKIES_PATH = ROOT_DIR / "cookies"


class Envs(str, Enum):
    PROD = "PROD"
    DEV = "DEV"


class TaskStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"


class ProduceMode(str, Enum):
    TODAY = "today"
    DATE_RANGE = "date_range"

    @classmethod
    def get_enum(cls, value: str) -> "ProduceMode":
        return cls._value2member_map_[value]  # type: ignore
