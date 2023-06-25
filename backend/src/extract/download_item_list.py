import json
from pathlib import Path

import httpx
from httpx import HTTPStatusError
from loguru import logger

from src.settings import Settings


def _prepare_payload(year: int) -> dict:
    # Form data is copied from the request produced by naviating to the page in Firefox
    payload_json = Path(__file__).parent / "payload_item_list.json"
    with open(payload_json, "r") as f:
        payload: dict = json.loads(f.read())
    payload.update({"ctl00$MainContent$rdSpecYear": str(year)[-2:]})

    return payload


def _download_item_list(settings: Settings, year: int) -> None:
    url = settings.download_item_list_url
    payload = _prepare_payload(year)
    try:
        r = httpx.post(url, data=payload)
        r.raise_for_status()
    except HTTPStatusError:
        logger.warning(f"DOWNLOAD: Download failed. Status code: {r.status_code}")
        return

    settings.raw_item_list_dir.mkdir(parents=True, exist_ok=True)
    filepath = settings.raw_item_list_dir / f"item_list_{year}.csv"
    with open(filepath, "w") as f:
        f.write(r.text)


def _existing_item_lists(settings: Settings) -> set[str]:
    files = settings.raw_item_list_dir.glob("*.csv")
    return {f.name for f in files}


def download_item_list_csv(settings: Settings, year: int) -> None:
    filepath = settings.raw_item_list_dir / f"item_list_{year}.csv"
    if filepath.name in _existing_item_lists(settings):
        logger.info("DOWNLOAD: Item list already downloaded")
        return

    logger.info(f"DOWNLOAD: Downloading item list for spec year {year}")
    _download_item_list(settings, year)
