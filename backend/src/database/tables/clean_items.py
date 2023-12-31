from pathlib import Path

from duckdb import DuckDBPyConnection

tablename = "clean_items"


def create_or_replace_table(con: DuckDBPyConnection, parquets: set[Path]) -> None:
    query = f"""
        CREATE OR REPLACE TABLE {tablename} AS (
            SELECT * FROM read_parquet( $files )
        )"""
    params = {"files": [str(p) for p in parquets]}
    con.execute(query, params)
