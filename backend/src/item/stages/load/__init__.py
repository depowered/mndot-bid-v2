from functools import partial

from loguru import logger

from src.database import db
from src.database.tables import item_pipeline, raw_items
from src.settings import Settings

previous_stage_complete_years = partial(
    item_pipeline.get_years_with_status,
    stage=item_pipeline.Stage.CLEAN,
    status=item_pipeline.Status.COMPLETE,
)

current_stage_not_run_years = partial(
    item_pipeline.get_years_with_status,
    stage=item_pipeline.Stage.LOAD,
    status=item_pipeline.Status.NOT_RUN,
)

current_stage_failed_years = partial(
    item_pipeline.get_years_with_status,
    stage=item_pipeline.Stage.LOAD,
    status=item_pipeline.Status.FAILED,
)

set_load_status_to_complete = partial(
    item_pipeline.update_status,
    stage=item_pipeline.Stage.LOAD,
    status=item_pipeline.Status.COMPLETE,
)

set_load_status_to_failed = partial(
    item_pipeline.update_status,
    stage=item_pipeline.Stage.LOAD,
    status=item_pipeline.Status.FAILED,
)


def run(settings: Settings) -> None:
    """Load all cleaned parquet files into database tables"""
    con = db.get_db_con()

    ready = previous_stage_complete_years(con=con)
    logger.info(f"LOAD: Loading data from {len(ready)} item lists")

    parquets = {
        settings.clean_item_list_dir / f"item_list_{year}.parquet" for year in ready
    }
    raw_items.create_or_replace_table(con, parquets)
    for year in ready:
        set_load_status_to_complete(con=con, spec_year=year)


def done() -> bool:
    """Returns a bool indicating if the stage needs to be run"""
    return False  # always run the load stage when called
