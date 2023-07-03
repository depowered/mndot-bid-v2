import sys

from loguru import logger

from src.abstract.stages.scrape.scrape_contract_ids import (
    ScrapeError,
    scrape_contract_ids,
)
from src.database import db
from src.database.tables import abstract_pipeline
from src.settings import Settings


def run(settings: Settings, year: int) -> None:
    """Scrapes contract ids for the given year and inserts them into the database."""
    logger.info(f"SCRAPE: Scraping contract ids for {year}")
    try:
        contract_ids = scrape_contract_ids(settings, year)
    except ScrapeError as e:
        logger.error(f"SCRAPE: {e.args[0]}")
        sys.exit(1)

    con = db.get_db_con()
    abstract_pipeline.insert_new_records(con, contract_ids)


def done() -> bool:
    """Returns a bool indicating if the stage needs to be run"""
    return False  # always run the scrape stage when called
