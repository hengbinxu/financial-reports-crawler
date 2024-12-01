from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from src.database.client import sql_connector
from src.database.repository import GoogleOauthScopesRepository
from src.utils.logger import SystemLogger
from src.utils.type_alias import StrPath
from src.utils.utils import HelperFunc


class GoogleOauth:
    SCOPES = [
        "https://www.googleapis.com/auth/drive.metadata.readonly",
        "https://www.googleapis.com/auth/drive.file",
    ]
    GOOGLE_SECRET_KEY_DIR = HelperFunc.get_root_dir() / "google-secret-keys"
    CREDENTIAL_PATH = GOOGLE_SECRET_KEY_DIR / "credentials.json"
    TOKEN_PATH = GOOGLE_SECRET_KEY_DIR / "token.json"
    log = SystemLogger.get_logger()

    def __init__(
        self,
        credential_path: StrPath | None = None,
        token_path: StrPath | None = None,
    ) -> None:
        self.credential_path = credential_path or self.CREDENTIAL_PATH
        self.token_path = token_path or self.TOKEN_PATH
        self.google_oauth_scopes_repo = GoogleOauthScopesRepository()

    def add_scopes(cls, scopes: List[str]) -> None:
        cls.SCOPES.extend(scopes)

    def remove_scopes(cls, scopes: List[str]) -> None:
        for scope in scopes:
            cls.SCOPES.remove(scope)

    def _is_scopes_changed(self) -> bool:
        with sql_connector.start_session() as session:
            db_hashed_scopes = self.google_oauth_scopes_repo.get(session)

        current_hashed_scopes = HelperFunc.hash_list(self.SCOPES)
        if db_hashed_scopes is None:
            with sql_connector.start_session() as session:
                self.google_oauth_scopes_repo.insert(
                    session, hashed_scopes=current_hashed_scopes
                )
            return True

        if db_hashed_scopes != current_hashed_scopes:
            with sql_connector.start_session() as session:
                self.google_oauth_scopes_repo.update(
                    session, hashed_scopes=current_hashed_scopes
                )
            self.log.debug("Scopes have been changed")
            return True
        return False

    def get_credentials(self) -> Credentials:
        creds: Credentials | None = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if self.token_path.exists():  # type: ignore
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if (
                creds
                and creds.expired
                and creds.refresh_token
                and self._is_scopes_changed() is False
            ):
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credential_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            HelperFunc.write_file(path=self.token_path, data=creds.to_json())
        return creds
