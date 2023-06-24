import json
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from httpx import HTTPStatusError

from src.settings import Settings


def _prepare_payload(year: int) -> dict:
    # Form data is copied from the request produced by naviating to the page in Firefox
    payload_json = Path(__file__).parent / "payload.json"
    with open(payload_json, "r") as f:
        payload: dict = json.loads(f.read())
    payload.update({"ctl00$MainContent$drpLettingYear": str(year)})
    return payload


def scrape_contract_ids(settings: Settings, year: int) -> set[int]:
    try:
        payload = _prepare_payload(year)
        url = settings.mndot_abstracts_app
        r = httpx.post(url, data=payload)
        r.raise_for_status()
    except HTTPStatusError as e:
        raise e

    contract_ids: set[int] = set()

    # Parse "Contract Id" column from html table
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


if __name__ == "__main__":
    settings = Settings()
    print(scrape_contract_ids(settings, 2023))
