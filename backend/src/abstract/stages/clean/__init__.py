from functools import partial

from loguru import logger

from src.abstract.stages.clean.clean_bid import clean_bid_csv
from src.abstract.stages.clean.clean_bidder import clean_bidder_csv
from src.abstract.stages.clean.clean_contract import clean_contract_csv
from src.abstract.stages.clean.validate import ValidationError
from src.database import abstract_pipeline, db
from src.settings import Settings

previous_stage_complete_ids = partial(
    abstract_pipeline.get_ids_with_status,
    stage=abstract_pipeline.Stage.SPLIT,
    status=abstract_pipeline.Status.COMPLETE,
)

current_stage_not_run_ids = partial(
    abstract_pipeline.get_ids_with_status,
    stage=abstract_pipeline.Stage.CLEAN,
    status=abstract_pipeline.Status.NOT_RUN,
)

set_clean_status_to_complete = partial(
    abstract_pipeline.update_status,
    stage=abstract_pipeline.Stage.CLEAN,
    status=abstract_pipeline.Status.COMPLETE,
)

set_clean_status_to_failed = partial(
    abstract_pipeline.update_status,
    stage=abstract_pipeline.Stage.CLEAN,
    status=abstract_pipeline.Status.FAILED,
)


def run(settings: Settings) -> None:
    """Clean subtable CSVs and writes results to parquet"""
    con = db.get_db_con()

    ready = previous_stage_complete_ids(con=con)
    not_run = current_stage_not_run_ids(con=con)
    ids = {id for id in not_run if id in ready}

    logger.info(f"CLEAN: Cleaning subtables for {len(ids)} Abstracts")
    for contract_id in ids:
        try:
            clean_contract_csv(settings, contract_id)
            clean_bid_csv(settings, contract_id)
            clean_bidder_csv(settings, contract_id)
            set_clean_status_to_complete(con=con, contract_id=contract_id)
        except ValidationError as e:
            set_clean_status_to_failed(con=con, contract_id=contract_id)
            logger.warning(f"CLEAN: {e.args[0]}")


def done() -> bool:
    """Returns a bool indicating if the stage needs to be run"""
    con = db.get_db_con()
    ready = previous_stage_complete_ids(con=con)
    not_run = current_stage_not_run_ids(con=con)
    ids = {id for id in not_run if id in ready}

    count = len(ids)
    if count < 1:
        logger.info("CLEAN: No abstract subtables to clean. Skipping stage.")
    return count < 1
