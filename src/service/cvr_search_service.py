from httpx._types import HeaderTypes

from src.models.cvr_search import GetCompanyInfoByCvrNumberResponse
from src.utils.base_client import BaseClient
from src.utils.base_router import Router, UrlPath
from src.utils.config import settings
from src.utils.cookie_manager import CookieManager

_cvr_search_routers = Router(
    [
        UrlPath(
            name="cvr_search_website",
            path=settings.CVR_SEARCH_WEBSITE_URL,
        ),
        UrlPath(
            name="cvr_search_api",
            path=settings.CVR_SEARCH_API,
        ),
    ]
)


class CvrSearchService(BaseClient):
    def __init__(self) -> None:
        super().__init__(url_router=_cvr_search_routers)
        self.cookie_manager = CookieManager(
            self._get_api_url(api_name="cvr_search_website")
        )

    def get_headers(self) -> HeaderTypes:
        return {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
            "priority": "u=1, i",
            "sec-ch-ua": (
                '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"'
            ),
            "sec-ch-ua-arch": '"arm"',
            "sec-ch-ua-bitness": '"64"',
            "sec-ch-ua-full-version": '"140.0.7339.214"',
            "sec-ch-ua-full-version-list": (
                '"Chromium";v="140.0.7339.214", "Not=A?Brand";v="24.0.0.0", '
                '"Google Chrome";v="140.0.7339.214"'
            ),
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": '""',
            "sec-ch-ua-platform": '"macOS"',
            "sec-ch-ua-platform-version": '"15.1.0"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            ),
            "Cookie": self._get_cookies(),
        }

    def _get_cookies(self) -> str:
        if (
            self.cookie_manager.is_cookies_present() is False
            or self.cookie_manager.is_cookies_expired()
        ):
            cookies = self.cookie_manager.save_cookies()
        else:
            cookies = self.cookie_manager.read_cookies()
        return cookies.value

    def get_company_info_by_cvr_num(
        self, cvr_number: str
    ) -> GetCompanyInfoByCvrNumberResponse:
        response = self.get(
            api_name="cvr_search_api",
            query_params={"cvrnummer": cvr_number, "locale": "en"},
            headers=self.get_headers(),
        )
        return GetCompanyInfoByCvrNumberResponse(**response.json())
