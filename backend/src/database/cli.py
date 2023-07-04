import os
import sys
from pathlib import Path

import click
from loguru import logger

from src.database import db
from src.settings import Settings


def _verify_db_not_exists(settings: Settings) -> None:
    if settings.db.exists():
        logger.warning(f"{settings.db.name} already exists. Exiting...")
        sys.exit(1)


def _verify_db_exists(settings: Settings) -> None:
    if not settings.db.exists():
        logger.warning(f"{settings.db.name} does not exist. Exiting...")
        sys.exit(1)


@click.group(help="Database management commands")
def database() -> None:
    pass


@database.command()
def create() -> None:
    """Create an empty database"""
    settings = Settings()
    _verify_db_not_exists(settings)
    db.init_db()
    logger.info(f"Created database: {settings.db}")


@database.command()
def delete() -> None:
    """Delete the database"""
    settings = Settings()
    _verify_db_exists(settings)
    os.remove(settings.db)
    logger.info(f"DELETED database: {settings.db}")


@database.command()
@click.argument(
    "output-dir",
    nargs=1,
    required=True,
    type=click.Path(exists=True, path_type=Path, file_okay=False, dir_okay=True),
)
def dump(output_dir: Path) -> None:
    """Dump all tables as parquet to the specified directory"""
    settings = Settings()
    _verify_db_exists(settings)
    db.copy_tables_to_parquet(output_dir)
    logger.info(f"Wrote parquets to: {output_dir}")


@database.command()
def dump_dbt_source() -> None:
    """Dump all tables as parquet to the dbt_source_dir"""
    settings = Settings()
    _verify_db_exists(settings)
    output_dir = settings.dbt_source_dir
    db.copy_tables_to_parquet(output_dir)
    logger.info(f"Wrote parquets to: {output_dir}")


@database.command()
@click.argument(
    "parquets", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path)
)
def load(parquets: tuple[Path]) -> None:
    """Load table from parquet"""
    settings = Settings()
    _verify_db_exists(settings)
    db.load_tables_from_dump(parquets)
    tables = [p.stem for p in parquets]
    logger.info(f"LOADED tables: {tables}")
