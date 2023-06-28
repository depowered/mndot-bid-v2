from pathlib import Path
import duckdb

from src.settings import Settings


def init_db(settings: Settings) -> None:
    """Creates an empty duckdb database with tables and types defined in init_db.sql"""
    con = duckdb.connect(str(settings.db))
    parent_dir = Path(__file__).resolve().parent
    with open(parent_dir / "init_db.sql", "r") as f:
        query = f.read()
    con.execute(query)
