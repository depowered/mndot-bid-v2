import sys
import os

import click
from loguru import logger

from src.db.init_db import init_db
from src.settings import Settings


@click.group(help="Database management commands")
def database() -> None:
    pass


@database.command()
def create() -> None:
    """Create an empty database"""
    settings = Settings()
    if settings.db.exists():
        logger.warning(f"{settings.db.name} already exists. Exiting...")
        sys.exit(1)
    init_db(settings)
    logger.info(f"Created database: {settings.db}")


@database.command()
def delete() -> None:
    """Delete the database"""
    settings = Settings()
    if not settings.db.exists():
        logger.warning(f"{settings.db.name} does not exist. Exiting...")
        sys.exit(1)
    os.remove(settings.db)
    logger.info(f"DELETED database: {settings.db}")
