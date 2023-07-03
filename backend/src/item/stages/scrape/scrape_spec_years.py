import httpx
from bs4 import BeautifulSoup
from httpx import HTTPStatusError, Response, TimeoutException

from src.settings import Settings


class ScrapeError(BaseException):
    pass


def _fetch_html(url: str) -> Response:
    try:
        r = httpx.get(url)
        r.raise_for_status()
        return r

    except HTTPStatusError as e:
        raise ScrapeError(
            f"Request failed with status code {e.response.status_code}"
        ) from e

    except TimeoutException as e:
        raise ScrapeError("Request timed out") from e


# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
# pyright: reportGeneralTypeIssues=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportUnknownArgumentType=false
def _parse_html(r: Response) -> set[int]:
    spec_years: set[int] = set()
    try:
        soup = BeautifulSoup(r.content, "html.parser")
        span = soup.find("span", id="MainContent_rdSpecYear")
        labels = span.find_all("label")
        for label in labels:
            # Label format: "Spec Year 2018"
            # Extract year as int
            year = int(label.text.strip()[-4:])
            spec_years.add(year)
        return spec_years

    except AttributeError as e:
        raise ScrapeError("Failed to parse HTML") from e


def scrape_spec_years(settings: Settings) -> set[int]:
    url = settings.download_item_list_url

    try:
        r = _fetch_html(url)
        return _parse_html(r)

    except ScrapeError as e:
        raise e
