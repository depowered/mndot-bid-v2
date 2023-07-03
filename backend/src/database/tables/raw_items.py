from pathlib import Path

from duckdb import DuckDBPyConnection

__tablename__ = "raw_items"


def create_or_replace_table(con: DuckDBPyConnection, parquets: set[Path]) -> None:
    query = f"""
        CREATE OR REPLACE TABLE {__tablename__} AS (
            SELECT * FROM read_parquet( $files )
        )"""
    params = {"files": [str(p) for p in parquets]}
    con.execute(query, params)
