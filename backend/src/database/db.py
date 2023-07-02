import duckdb
from duckdb import DuckDBPyConnection

from src.database.tables import abstract_pipeline, item_pipeline
from src.database.types import status
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
