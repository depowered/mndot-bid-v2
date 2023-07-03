from functools import partial

from loguru import logger

from src.database import db
from src.database.tables import item_pipeline
from src.item.stages.download.download_item_list import (
    DownloadError,
    download_item_list_csv,
)
from src.settings import Settings

get_years_to_download = partial(
    item_pipeline.get_years_with_status,
    stage=item_pipeline.Stage.DOWNLOAD,
    status=item_pipeline.Status.NOT_RUN,
)

set_download_status_to_complete = partial(
    item_pipeline.update_status,
    stage=item_pipeline.Stage.DOWNLOAD,
    status=item_pipeline.Status.COMPLETE,
)

set_download_status_to_failed = partial(
    item_pipeline.update_status,
    stage=item_pipeline.Stage.DOWNLOAD,
    status=item_pipeline.Status.FAILED,
)


def run(settings: Settings) -> None:
    """Downloads Abstract CSVs"""
    con = db.get_db_con()
    spec_years = get_years_to_download(con=con)
    logger.info(f"DOWNLOAD: Downloading {len(spec_years)} item list CSVs")
    for year in spec_years:
        try:
            download_item_list_csv(settings, year)
            set_download_status_to_complete(con=con, spec_year=year)
        except DownloadError as e:
            set_download_status_to_failed(con=con, spec_year=year)
            logger.warning(f"DOWNLOAD: {e.args[0]}")


def done() -> bool:
    """Returns a bool indicating if the stage needs to be run"""
    con = db.get_db_con()
    spec_years = get_years_to_download(con=con)
    count = len(spec_years)
    if count < 1:
        logger.info("DOWNLOAD: No item list CSVs to download. Skipping stage.")
    return count < 1
