import httpx
from loguru import logger

from src.settings import Settings


def _download_abstract_csv(settings: Settings, contract_id: int) -> None:
    url = settings.download_abstract_url
    params = {"ContractId": contract_id}
    try:
        r = httpx.get(url, params=params)
        r.raise_for_status()
    except httpx.HTTPStatusError:
        logger.warning(
            f"DOWNLOAD: Failed to download abstract {contract_id}. Status code: {r.status_code}"
        )
        return

    settings.raw_abstract_dir.mkdir(parents=True, exist_ok=True)
    filepath = settings.raw_abstract_dir / f"{contract_id}.csv"
    with open(filepath, "w") as f:
        f.write(r.text)


def _existing_abstracts(settings: Settings) -> set[int]:
    files = settings.raw_abstract_dir.glob("*.csv")
    return {int(f.stem) for f in files}


def download_abstract_csvs(settings: Settings, contract_ids: set[int]) -> None:
    # skip abstracts that are already downloaded
    download = contract_ids - _existing_abstracts(settings)
    count = len(download)
    if count < 1:
        logger.info("DOWNLOAD: Abstracts already downloaded.")
        return

    logger.info(f"DOWNLOAD: Downloading {count} abstracts")
    for idx, contract_id in enumerate(download):
        logger.info(
            f"DOWNLOAD: Downloading abstract: {contract_id} ({idx + 1} of {count})"
        )
        _download_abstract_csv(settings, contract_id)
