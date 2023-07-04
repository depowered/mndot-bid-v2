import os
import sys
from pathlib import Path

import click
from loguru import logger

from src.database import db
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
    db.init_db()
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


@database.command()
def dump() -> None:
    """Dump all tables to parquet"""
    settings = Settings()
    if not settings.db.exists():
        logger.warning(f"{settings.db.name} does not exist. Exiting...")
        sys.exit(1)
    db.dump_tables(output_dir=settings.db_dump_dir)
    logger.info(f"DUMPED tables to: {settings.db_dump_dir}")


@database.command()
def write_dbt_source() -> None:
    """Dump select tables to dbt_source dir as parquet"""
    settings = Settings()
    if not settings.db.exists():
        logger.warning(f"{settings.db.name} does not exist. Exiting...")
        sys.exit(1)
    db.write_dbt_source(output_dir=settings.dbt_source_dir)
    logger.info(f"Wrote parquets to: {settings.dbt_source_dir}")


@database.command()
@click.argument(
    "parquets", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path)
)
def load(parquets: tuple[Path]) -> None:
    """Load table from parquet"""
    settings = Settings()
    if not settings.db.exists():
        logger.warning(f"{settings.db.name} does not exist. Exiting...")
        sys.exit(1)
    db.load_tables_from_dump(parquets)
    tables = [p.stem for p in parquets]
    logger.info(f"LOADED tables: {tables}")
