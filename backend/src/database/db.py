import duckdb
from duckdb import DuckDBPyConnection

from src.database.tables import abstract_pipeline
from src.settings import Settings


def get_db_con() -> DuckDBPyConnection:
    settings = Settings()
    return duckdb.connect(str(settings.db))


def init_db() -> None:
    """Creates an empty duckdb database with tables and types defined in init_db.sql"""
    con = get_db_con()
    abstract_pipeline.create_status_type(con)
    abstract_pipeline.create_table(con)
