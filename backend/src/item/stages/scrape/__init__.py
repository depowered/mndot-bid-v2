import sys

from loguru import logger

from src.database import db
from src.database.tables import item_pipeline
from src.item.stages.scrape.scrape_spec_years import (
    ScrapeError,
    scrape_spec_years,
)
from src.settings import Settings


def run(settings: Settings):
    """Scrapes available item list spec years and inserts them into the database."""
    logger.info("SCRAPE: Scraping item list spec years")
    try:
        spec_years = scrape_spec_years(settings)
    except ScrapeError as e:
        logger.error(f"SCRAPE: {e.args[0]}")
        sys.exit(1)

    con = db.get_db_con()
    item_pipeline.insert_new_records(con, spec_years)


def done() -> bool:
    """Returns a bool indicating if the stage needs to be run"""
    return False  # always run the scrape stage when called
