from pydantic_settings import BaseSettings, SettingsConfigDict

from src.utils.constants import Envs
from src.utils.utils import HelperFunc

ENV_PATH = HelperFunc.get_root_dir() / "envs/.env"


class Settings(BaseSettings):
    ENV: Envs
    DENMARK_REPORT_URL: str
    DENMARK_CVR_API_ULR: str
    DB_URL: str
    DENMARK_PARENT_DRIVE_ID: str

    model_config = SettingsConfigDict(env_file=ENV_PATH)


settings = Settings()
