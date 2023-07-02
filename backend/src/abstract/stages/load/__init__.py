from functools import partial

from loguru import logger

from src.abstract.stages.load.load_tables import (
    load_raw_bidders,
    load_raw_bids,
    load_raw_contracts,
)
from src.database import abstract_pipeline, db, raw_bidders, raw_bids, raw_contracts
from src.settings import Settings

previous_stage_complete_ids = partial(
    abstract_pipeline.get_ids_with_status,
    stage=abstract_pipeline.Stage.CLEAN,
    status=abstract_pipeline.Status.COMPLETE,
)

current_stage_not_run_ids = partial(
    abstract_pipeline.get_ids_with_status,
    stage=abstract_pipeline.Stage.LOAD,
    status=abstract_pipeline.Status.NOT_RUN,
)

current_stage_failed_ids = partial(
    abstract_pipeline.get_ids_with_status,
    stage=abstract_pipeline.Stage.LOAD,
    status=abstract_pipeline.Status.FAILED,
)

set_load_status_to_complete = partial(
    abstract_pipeline.update_status,
    stage=abstract_pipeline.Stage.LOAD,
    status=abstract_pipeline.Status.COMPLETE,
)

set_load_status_to_failed = partial(
    abstract_pipeline.update_status,
    stage=abstract_pipeline.Stage.LOAD,
    status=abstract_pipeline.Status.FAILED,
)


def run(settings: Settings) -> None:
    """Load all cleaned parquet files into database tables"""
    con = db.get_db_con()

    ready = previous_stage_complete_ids(con=con)
    failed = current_stage_failed_ids(con=con)
    load = ready - failed

    logger.info(f"LOAD: Loading data from {len(load)} Abstracts")

    load_raw_contracts(con, settings, load)
    load_raw_bids(con, settings, load)
    load_raw_bidders(con, settings, load)

    # Verify that all contracts ids appear in each table
    # Set status to failed and remove records for any ids that fail check
    missing_from_contracts = load - raw_contracts.get_all_contract_ids(con)
    missing_from_bids = load - raw_bids.get_all_contract_ids(con)
    missing_from_bidders = load - raw_bidders.get_all_contract_ids(con)
    missing = missing_from_contracts | missing_from_bids | missing_from_bidders
    if missing:
        logger.warning(f"LOAD: Failed to load ids: {missing}")
        raw_contracts.delete_contract_ids(con, missing)
        raw_bids.delete_contract_ids(con, missing)
        raw_bidders.delete_contract_ids(con, missing)
        for id in missing:
            set_load_status_to_failed(con=con, contract_id=id)

    complete = load - missing
    for id in complete:
        set_load_status_to_complete(con=con, contract_id=id)


def done() -> bool:
    """Returns a bool indicating if the stage needs to be run"""
    con = db.get_db_con()
    ready = previous_stage_complete_ids(con=con)
    not_run = current_stage_not_run_ids(con=con)
    ids = {id for id in not_run if id in ready}

    count = len(ids)
    if count < 1:
        logger.info("LOAD: No new data to load. Skipping stage.")
    return count < 1
