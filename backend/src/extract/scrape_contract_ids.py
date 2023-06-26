import json
import sys
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from httpx import HTTPStatusError, Response
from loguru import logger

from src.settings import Settings


def _prepare_payload(year: int) -> dict:
    # Form data is copied from the request produced by naviating to the page in Firefox
    payload_json = Path(__file__).parent / "payload_abstract.json"
    with open(payload_json, "r") as f:
        payload: dict = json.loads(f.read())
    payload.update({"ctl00$MainContent$drpLettingYear": str(year)})
    return payload


def _fetch_html(url: str, payload: dict) -> Response:
    try:
        r = httpx.post(url, data=payload)
        r.raise_for_status()
        return r
    except HTTPStatusError:
        logger.warning(
            f"SCRAPE: Scraping failed with status code {r.status_code}. Exiting..."
        )
        sys.exit(1)


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
    except AttributeError as e:
        logger.warning(f"SCRAPE: Parsing failed with error: {e}")
        sys.exit(1)

    return contract_ids


def scrape_contract_ids(settings: Settings, year: int) -> set[int]:
    payload = _prepare_payload(year)
    url = settings.mndot_abstracts_app

    logger.info(f"SCRAPE: Scraping contract ids for {year}")
    r = _fetch_html(url, payload)

    logger.info("SCRAPE: Parsing html")
    return _parse_html(r)
