import sys

from loguru import logger

from src.abstract.stages.scrape.scrape_contract_ids import (
    ScrapeError,
    scrape_contract_ids,
)
from src.database import db, pipeline_status
from src.settings import Settings


def run(settings: Settings, year: int) -> None:
    """Scrapes contract ids for the given year and inserts them into the database."""
    logger.info(f"SCRAPE: Scraping contract ids for {year}")
    try:
        contract_ids = scrape_contract_ids(settings, year)
    except ScrapeError as e:
        logger.error("SCRAPE: Stage raised an error")
        logger.error(e)
        sys.exit(1)

    logger.info("SCRAPE: Loading database")
    pipeline_status.insert_new_records(con=db.get_db_con(), contract_ids=contract_ids)
