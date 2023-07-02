from functools import partial

from loguru import logger

from src.abstract.stages.download.download_abstract import (
    DownloadError,
    download_abstract_csv,
)
from src.database import abstract_pipeline, db
from src.settings import Settings

get_ids_to_download = partial(
    abstract_pipeline.get_ids_with_status,
    stage=abstract_pipeline.Stage.DOWNLOAD,
    status=abstract_pipeline.Status.NOT_RUN,
)

set_download_status_to_complete = partial(
    abstract_pipeline.update_status,
    stage=abstract_pipeline.Stage.DOWNLOAD,
    status=abstract_pipeline.Status.COMPLETE,
)

set_download_status_to_failed = partial(
    abstract_pipeline.update_status,
    stage=abstract_pipeline.Stage.DOWNLOAD,
    status=abstract_pipeline.Status.FAILED,
)


def run(settings: Settings) -> None:
    """Downloads Abstract CSVs"""
    con = db.get_db_con()
    contract_ids = get_ids_to_download(con=con)
    logger.info(f"DOWNLOAD: Downloading {len(contract_ids)} Abstract CSVs")
    for contract_id in contract_ids:
        try:
            download_abstract_csv(settings, contract_id)
            set_download_status_to_complete(con=con, contract_id=contract_id)
        except DownloadError as e:
            set_download_status_to_failed(con=con, contract_id=contract_id)
            logger.warning(f"DOWNLOAD: {e.args[0]}")


def done() -> bool:
    """Returns a bool indicating if the stage needs to be run"""
    contract_ids = get_ids_to_download(db.get_db_con())
    count = len(contract_ids)
    if count < 1:
        logger.info("DOWNLOAD: No Abstract CSVs to download. Skipping stage.")
    return count < 1
