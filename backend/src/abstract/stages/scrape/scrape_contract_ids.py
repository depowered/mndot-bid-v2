import json
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from httpx import HTTPStatusError, Response, TimeoutException

from src.settings import Settings


class ScrapeError(BaseException):
    pass


Payload = dict[str, str]


def _prepare_payload(year: int) -> Payload:
    # Form data is copied from the request produced by naviating to the page in Firefox
    payload_json = Path(__file__).parent / "payload_abstract.json"
    with open(payload_json, "r") as f:
        payload: Payload = json.loads(f.read())
    payload.update({"ctl00$MainContent$drpLettingYear": str(year)})
    return payload


def _fetch_html(url: str, payload: Payload) -> Response:
    try:
        r = httpx.post(url, data=payload)
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
    contract_ids: set[int] = set()
    try:
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table", id="MainContent_gvabstractMenu")
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 7:
                continue  # skip header and footer
            # "Contract Id is the third column of the html table"
            contract_ids.add(int(cells[2].string))
        return contract_ids

    except AttributeError as e:
        raise ScrapeError("Failed to parse HTML") from e


def scrape_contract_ids(settings: Settings, year: int) -> set[int]:
    payload = _prepare_payload(year)
    url = settings.mndot_abstracts_app

    try:
        r = _fetch_html(url, payload)
        return _parse_html(r)

    except ScrapeError as e:
        raise e
