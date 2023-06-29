from functools import partial

from loguru import logger

from src.abstract.stages.split.split_abstracts import SplitError, split_abstract_csv
from src.database import db, pipeline_status
from src.settings import Settings

previous_stage_complete_ids = partial(
    pipeline_status.get_ids_with_status,
    stage=pipeline_status.Stage.DOWNLOAD,
    status=pipeline_status.Status.COMPLETE,
)

current_stage_not_run_ids = partial(
    pipeline_status.get_ids_with_status,
    stage=pipeline_status.Stage.SPLIT,
    status=pipeline_status.Status.NOT_RUN,
)

set_split_status_to_complete = partial(
    pipeline_status.update_status,
    stage=pipeline_status.Stage.SPLIT,
    status=pipeline_status.Status.COMPLETE,
)

set_split_status_to_failed = partial(
    pipeline_status.update_status,
    stage=pipeline_status.Stage.SPLIT,
    status=pipeline_status.Status.FAILED,
)


def run(settings: Settings) -> None:
    """Splits Abstract CSVs into their subtables"""
    con = db.get_db_con()

    ready = previous_stage_complete_ids(con=con)
    not_run = current_stage_not_run_ids(con=con)
    ids = {id for id in not_run if id in ready}

    logger.info(f"SPLIT: Splitting {len(ids)} Abstract CSVs")
    for contract_id in ids:
        try:
            split_abstract_csv(settings=settings, contract_id=contract_id)
            set_split_status_to_complete(con=con, contract_id=contract_id)
        except SplitError as e:
            set_split_status_to_failed(con=con, contract_id=contract_id)
            logger.warning(f"SPLIT: {e.args[0]}")


def done() -> bool:
    """Returns a bool indicating if the stage needs to be run"""
    con = db.get_db_con()
    ready = previous_stage_complete_ids(con=con)
    not_run = current_stage_not_run_ids(con=con)
    ids = {id for id in not_run if id in ready}

    count = len(ids)
    if count < 1:
        logger.info("SPLIT: No Abstract CSVs to split. Skipping stage.")
    return count < 1
