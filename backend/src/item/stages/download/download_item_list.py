import json
from pathlib import Path

import httpx
from httpx import HTTPStatusError

from src.settings import Settings


class DownloadError(BaseException):
    pass


Payload = dict[str, str]


def _prepare_payload(year: int) -> Payload:
    # Form data is copied from the request produced by naviating to the page in Firefox
    payload_json = Path(__file__).parent / "payload_item_list.json"
    with open(payload_json, "r") as f:
        payload: Payload = json.loads(f.read())
    payload.update({"ctl00$MainContent$rdSpecYear": str(year)[-2:]})

    return payload


def download_item_list_csv(settings: Settings, year: int) -> None:
    url = settings.download_item_list_url
    payload = _prepare_payload(year)
    try:
        r = httpx.post(url, data=payload)
        r.raise_for_status()
    except HTTPStatusError as e:
        raise DownloadError(
            f"Failed to download item list for spec year {year}. Status code: {e.response.status_code}"
        ) from e

    settings.raw_item_list_dir.mkdir(parents=True, exist_ok=True)
    filepath = settings.raw_item_list_dir / f"item_list_{year}.csv"
    filepath.write_text(r.text)
