from typing import List

from pydantic import Field

from src.utils.base_model import BaseModel


class _File(BaseModel):
    id: str
    name: str
    mime_type: str = Field(alias="mimeType")


class ListFilesResponse(BaseModel):
    files: List[_File]


class CreateFolderResponse(BaseModel):
    id: str
    name: str
    kind: str
    mime_type: str = Field(alias="mimeType")


class UploadFileResponse(CreateFolderResponse):
    pass
