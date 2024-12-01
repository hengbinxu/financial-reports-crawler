from typing import Any, Dict

from httpx import Client, Request, Response
from httpx._types import HeaderTypes, QueryParamTypes

from src.utils.base_router import Router
from src.utils.logger import SystemLogger


class BaseClient:
    log = SystemLogger.get_logger()

    def __init__(self, *, url_router: Router) -> None:
        self.url_router = url_router
        self.client = Client(
            event_hooks={
                "request": [self._log_request],
                "response": [self._raise_for_status],
            }
        )

    def _log_request(self, request: Request) -> None:
        self.log.debug(
            f"Send Url: {request.url} with method: {request.method}, "
            f"headers: {request.headers}"
        )

    def _raise_for_status(self, response: Response) -> None:
        response.raise_for_status()

    def _get_api_url(
        self, *, api_name: str, path_params: Dict[str, Any] | None = None
    ) -> str:
        if path_params:
            return self.url_router.get_format_url(api_name, **path_params)
        return self.url_router.get_api_url(api_name)

    def get(
        self,
        *,
        api_name: str,
        path_params: Dict[str, Any] | None = None,
        query_params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        **kwargs: Any,
    ) -> Response:
        url = self._get_api_url(api_name=api_name, path_params=path_params)
        return self.client.get(url, params=query_params, headers=headers, **kwargs)

    def post(
        self,
        *,
        api_name: str,
        path_params: Dict[str, Any] | None = None,
        query_params: QueryParamTypes | None = None,
        json: Any | None = None,
        headers: HeaderTypes | None = None,
        **kwargs: Any,
    ) -> Response:
        url = self._get_api_url(api_name=api_name, path_params=path_params)
        return self.client.post(
            url, params=query_params, json=json, headers=headers, **kwargs
        )
