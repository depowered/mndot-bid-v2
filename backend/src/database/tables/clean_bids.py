from pathlib import Path

from duckdb import DuckDBPyConnection

tablename = "clean_bids"


def create_or_replace_table(con: DuckDBPyConnection, parquets: set[Path]) -> None:
    query = f"""
        CREATE OR REPLACE TABLE {tablename} AS (
            SELECT * FROM read_parquet( $files )
        )"""
    params = {"files": [str(p) for p in parquets]}
    con.execute(query, params)


def get_all_contract_ids(con: DuckDBPyConnection) -> set[int]:
    query = f"SELECT DISTINCT contract_id FROM {tablename}"
    records = con.execute(query).fetchall()
    return {row[0] for row in records}


def delete_contract_ids(con: DuckDBPyConnection, contract_ids: set[int]) -> None:
    query = f"DELETE FROM {tablename} WHERE contract_id IN {tuple(contract_ids)}"
    con.execute(query)
    con.commit()
