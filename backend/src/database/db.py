import duckdb
from duckdb import DuckDBPyConnection

from src.database import pipeline_status
from src.settings import Settings


def get_db_con() -> DuckDBPyConnection:
    settings = Settings()
    return duckdb.connect(str(settings.db))


def init_db() -> None:
    """Creates an empty duckdb database with tables and types defined in init_db.sql"""
    con = get_db_con()
    pipeline_status.create_status_type(con)
    pipeline_status.create_table(con)
