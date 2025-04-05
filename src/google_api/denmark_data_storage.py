from src.google_api.drive_api import GoogleDriveApi
from src.models.google_drive_api import CreateFolderResponse, ListFilesResponse
from src.utils.config import settings
from src.utils.type_alias import StrPath
from src.utils.utils import SynchronizedLock


class DenmarkDataStorage(GoogleDriveApi):
    def __init__(
        self,
        credential_path: StrPath | None = None,
        token_path: StrPath | None = None,
    ) -> None:
        super().__init__(credential_path, token_path)
        self.root_drive_id = settings.DENMARK_PARENT_DRIVE_ID

    @SynchronizedLock.lock()
    def list_root_directories(self) -> ListFilesResponse:
        return self.list_files(
            q="mimeType = 'application/vnd.google-apps.folder'",
            drive_id=self.root_drive_id,
        )

    @SynchronizedLock.lock()
    def list_directories(self, drive_id: str) -> ListFilesResponse:
        return self.list_files(
            q="mimeType = 'application/vnd.google-apps.folder'", drive_id=drive_id
        )

    @SynchronizedLock.lock()
    def create_folder_on_root(self, name: str) -> CreateFolderResponse:
        return self.create_folder(name=name, parent_drive_ids=[self.root_drive_id])

    def find_folder_id_by_name(
        self,
        *,
        folder_name: str,
        drive_id: str,
    ) -> str | None:
        response = self.list_directories(drive_id)
        for file in response.files:
            if file.name == folder_name:
                return file.id
        return None

    def find_root_path_folder_id_by_name(self, folder_name: str) -> str | None:
        return self.find_folder_id_by_name(
            folder_name=folder_name, drive_id=self.root_drive_id
        )
