from typing import List

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from src.google_api.oauth import GoogleOauth
from src.models.google_drive_api import (
    CreateFolderResponse,
    ListFilesResponse,
    UploadFileResponse,
)
from src.utils.params_collector import ParamsCollector
from src.utils.type_alias import StrPath


class GoogleDriveApi(GoogleOauth):
    def __init__(
        self,
        credential_path: StrPath | None = None,
        token_path: StrPath | None = None,
    ) -> None:
        super().__init__(credential_path, token_path)
        self.credentials = self.get_credentials()
        self.drive_service = build("drive", "v3", credentials=self.credentials)

    def list_files(
        self,
        *,
        q: str | None = None,
        drive_id: str | None = None,
        fields: str | None = "files(id, name, mimeType)",
        page_size: int = 10,
        **kwargs: str,
    ) -> ListFilesResponse:
        if drive_id:
            q = f"{q} and '{drive_id}' in parents" if q else f"'{drive_id}' in parents"
        params_collector = ParamsCollector()
        params_collector.add_param("q", q, exclude_none=True)
        params_collector.add_param("fields", fields, exclude_none=True)
        params_collector.add_param("pageSize", page_size)
        for key, value in kwargs.items():
            params_collector.add_param(key, value)
        results = self.drive_service.files().list(**params_collector.params).execute()
        return ListFilesResponse(**results)

    def create_folder(
        self,
        *,
        name: str,
        parent_drive_ids: List[str],
    ) -> CreateFolderResponse:
        folder_meta = {
            "name": name,
            "parents": parent_drive_ids,
            "mimeType": "application/vnd.google-apps.folder",
        }
        result = self.drive_service.files().create(body=folder_meta).execute()
        return CreateFolderResponse(**result)

    def upload_file(
        self,
        *,
        file_path: StrPath,
        parent_drive_ids: List[str],
    ) -> UploadFileResponse:
        file_meta = {
            "name": file_path.name,
            "parents": parent_drive_ids,
        }
        media_body = MediaFileUpload(filename=file_path)
        result = (
            self.drive_service.files()
            .create(body=file_meta, media_body=media_body)
            .execute()
        )
        return UploadFileResponse(**result)

    def delete_file(self, *, file_id: str) -> None:
        self.drive_service.files().delete(fileId=file_id).execute()
