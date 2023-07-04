from pathlib import Path
from typing import Sequence

import duckdb
from duckdb import CatalogException, DuckDBPyConnection

from src.database.tables import (
    abstract_pipeline,
    item_pipeline,
    raw_bidders,
    raw_bids,
    raw_contracts,
    raw_items,
)
from src.database.types import status
from src.database.views import failed_abstract_pipeline
from src.settings import Settings


def get_db_con() -> DuckDBPyConnection:
    settings = Settings()
    return duckdb.connect(str(settings.db))  # pyright: ignore reportUknownMember


def init_db() -> None:
    """Creates an empty duckdb database with tables and types defined in init_db.sql"""
    con = get_db_con()
    status.create_status_type(con)
    abstract_pipeline.create_table(con)
    item_pipeline.create_table(con)
    failed_abstract_pipeline.create_or_replace_view(con)


def copy_tables_to_parquet(output_dir: Path) -> None:
    tables = [
        abstract_pipeline.tablename,
        item_pipeline.tablename,
        raw_bidders.tablename,
        raw_bids.tablename,
        raw_contracts.tablename,
        raw_items.tablename,
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    con = get_db_con()
    for table in tables:
        parquet = output_dir / f"{table}.parquet"
        query = f"COPY {table} TO '{parquet}' (FORMAT PARQUET)"
        con.execute(query)


def load_tables_from_dump(parquets: Sequence[Path]) -> None:
    con = get_db_con()
    for parquet in parquets:
        table = parquet.stem
        try:
            query = f"COPY {table} FROM '{parquet}' (FORMAT PARQUET)"
            con.execute(query)
        except CatalogException:  # Raised if table doesn't exist
            query = f"CREATE TABLE {table} AS SELECT * FROM '{parquet}'"
            con.execute(query)
