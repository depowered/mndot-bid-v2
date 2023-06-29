import httpx

from src.settings import Settings


class DownloadError(BaseException):
    pass


def download_abstract_csv(settings: Settings, contract_id: int) -> None:
    url = settings.download_abstract_url
    params = {"ContractId": contract_id}
    try:
        r = httpx.get(url, params=params)
        r.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise DownloadError(
            f"Failed to download abstract {contract_id}. Status code: {e.response.status_code}"
        ) from e

    settings.raw_abstract_dir.mkdir(parents=True, exist_ok=True)
    filepath = settings.raw_abstract_dir / f"{contract_id}.csv"
    with open(filepath, "w") as f:
        f.write(r.text)
