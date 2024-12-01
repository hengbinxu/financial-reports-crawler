from sqlmodel import Field

from src.database.entity.base_model import BasePrimaryKeyModel


class GoogleOauthScopes(BasePrimaryKeyModel, table=True):  # type: ignore
    __tablename__ = "google_oauth_scopes"
    hashed_scopes: str = Field(nullable=False)
