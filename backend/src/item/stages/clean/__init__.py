from functools import partial

from loguru import logger

from src.database import db
from src.database.tables import item_pipeline
from src.item.stages.clean.clean_item_list import clean_item_list_csv
from src.item.stages.clean.validate import ValidationError
from src.settings import Settings

previous_stage_complete_years = partial(
    item_pipeline.get_years_with_status,
    stage=item_pipeline.Stage.DOWNLOAD,
    status=item_pipeline.Status.COMPLETE,
)

current_stage_not_run_years = partial(
    item_pipeline.get_years_with_status,
    stage=item_pipeline.Stage.CLEAN,
    status=item_pipeline.Status.NOT_RUN,
)

set_clean_status_to_complete = partial(
    item_pipeline.update_status,
    stage=item_pipeline.Stage.CLEAN,
    status=item_pipeline.Status.COMPLETE,
)

set_clean_status_to_failed = partial(
    item_pipeline.update_status,
    stage=item_pipeline.Stage.CLEAN,
    status=item_pipeline.Status.FAILED,
)


def run(settings: Settings):
    """Clean item list CSVs and write results to parquet"""
    con = db.get_db_con()

    ready = previous_stage_complete_years(con=con)
    not_run = current_stage_not_run_years(con=con)
    years = {year for year in not_run if year in ready}

    logger.info(f"CLEAN: Cleaning {len(years)} item lists")
    for year in years:
        try:
            clean_item_list_csv(settings, year)
            set_clean_status_to_complete(con=con, spec_year=year)
        except ValidationError as e:
            set_clean_status_to_failed(con=con, spec_year=year)
            logger.warning(f"CLEAN: {e.args[0]}")


def done() -> bool:
    """Returns a bool indicating if the stage needs to be run"""
    con = db.get_db_con()
    ready = previous_stage_complete_years(con=con)
    not_run = current_stage_not_run_years(con=con)
    years = {year for year in not_run if year in ready}

    count = len(years)
    if count < 1:
        logger.info("CLEAN: No item lists to clean. Skipping stage.")
    return count < 1
