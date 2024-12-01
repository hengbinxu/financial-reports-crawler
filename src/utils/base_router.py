from typing import Any, List

from pydantic import RootModel

from src.utils.base_model import BaseModel


class UrlPath(BaseModel):
    name: str
    path: str

    def format_url(self, **kwargs: Any) -> str:
        return self.path.format(**kwargs)


class Router(RootModel[List[UrlPath]]):
    def get_api_url(self, name: str) -> str:
        return next(router for router in self.root if router.name == name).path

    def get_format_url(self, name: str, **kwargs: Any) -> str:
        return next(router for router in self.root if router.name == name).format_url(
            **kwargs
        )
