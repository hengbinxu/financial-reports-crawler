import random
import time
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from DrissionPage import ChromiumOptions, ChromiumPage
from pydantic import RootModel

from src.utils.base_model import BaseModel
from src.utils.constants import COOKIES_PATH
from src.utils.logger import SystemLogger
from src.utils.utils import HelperFunc


class _Cookie(BaseModel):
    name: str
    value: str
    domain: str


class Cookies(RootModel[list[_Cookie]]):
    pass

    @property
    def value(self) -> str:
        cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in self.root])
        cookies += "; defaultLocale=en; cookieOptOut=y"
        return cookies


class CookieManager:
    def __init__(
        self, url: str, cookies_expired_secs: int = 600, load_page_timeout: int = 60
    ) -> None:
        COOKIES_PATH.mkdir(exist_ok=True)
        self.log = SystemLogger.get_logger()
        self.url = url
        self.cookies_fp = self._get_file_path()
        self.cookies_expired_secs = cookies_expired_secs
        self.load_page_timeout = load_page_timeout
        self.browser_options = self._set_browser_options()

    def _get_file_path(self) -> Path:
        file_name = HelperFunc.hash_str(self.url)
        return COOKIES_PATH / f"{file_name}.json"

    def _set_browser_options(self) -> ChromiumOptions:
        co = ChromiumOptions()
        co.incognito()
        return co

    @contextmanager
    def _session_page(self) -> Generator[ChromiumPage, None, None]:
        try:
            page = ChromiumPage(self.browser_options)
            yield page
        except Exception as e:
            raise e
        finally:
            page.quit()

    def get_cookies_from_page(self) -> Cookies:
        with self._session_page() as page:
            self.log.debug(f"Start getting the cookies from {self.url}")
            page.get(self.url)
            page.wait.load_start(timeout=self.load_page_timeout, raise_err=True)
            self._actions_to_get_cookies(page)
            cookies = page.cookies()
            time.sleep(random.uniform(2, 3))
        return Cookies(root=[_Cookie(**cookie) for cookie in cookies])

    def _actions_to_get_cookies(self, page: ChromiumPage) -> None:
        test_cvr_number = "37268461"
        self.log.debug(
            f"Start typing the cvr number: {test_cvr_number} to get full cookies"
        )
        input_cvr_num_ele = page.ele('xpath://*[@id="forside-soegefelt-id"]')
        input_cvr_num_ele.input(test_cvr_number)
        search_btn = page.ele(
            'xpath://*[@id="main-content"]/div[2]/div[1]/div/div/form/div/button[1]'
        )
        search_btn.click()
        page.wait.load_start(timeout=self.load_page_timeout, raise_err=True)

    def is_cookies_present(self) -> bool:
        return self.cookies_fp.exists()

    def is_cookies_expired(self) -> bool:
        stat_info = self.cookies_fp.stat()
        current_ts = int(HelperFunc.get_now().timestamp())
        if (current_ts - stat_info.st_mtime) >= self.cookies_expired_secs:
            return True
        return False

    def read_cookies(self) -> Cookies:
        return Cookies(
            [_Cookie(**cookie) for cookie in HelperFunc.read_json(self.cookies_fp)]
        )

    def save_cookies(self) -> Cookies:
        cookies = self.get_cookies_from_page()
        HelperFunc.write_json(path=self.cookies_fp, data=cookies.model_dump())
        return cookies
