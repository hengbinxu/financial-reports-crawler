import logging
import os
from pathlib import Path
from typing import Dict, Literal


class SystemLogger:
    _CURRENT: logging.Logger | None = None
    LOG_PATH = os.path.join(os.getcwd(), "logs")
    FMT = (
        "%(asctime)s [%(levelname)s] "
        "%(module)s:%(funcName)s "
        "(%(lineno)d) %(message)s"
    )
    FORMATTER = logging.Formatter(FMT, datefmt="%Y-%m-%d %H:%M:%S")
    LOG_LEVEL_MAP: Dict[str, int] = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }

    @classmethod
    def create_log_dir(cls) -> None:
        """
        Create a log directory if it doesn't exist
        """
        Path(cls.LOG_PATH).mkdir(parents=True, exist_ok=True)

    @classmethod
    def create_logger(
        cls,
        name: str,
        level: Literal["debug", "info", "warning", "error", "critical"] = "debug",
    ) -> logging.Logger:
        # cls.create_log_dir()
        logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        handler.setFormatter(cls.FORMATTER)
        logger.addHandler(handler)
        logger.setLevel(cls.LOG_LEVEL_MAP[level.lower()])
        return logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Ensuring the log instance is only created one time
        """
        if cls._CURRENT is None:
            cls._CURRENT = cls.create_logger(__name__)
        return cls._CURRENT
