from pathlib import Path

from duckdb import DuckDBPyConnection


def create_or_replace_table(con: DuckDBPyConnection, parquets: set[Path]) -> None:
    query = """
        CREATE OR REPLACE TABLE raw_bidders AS (
            SELECT * FROM read_parquet( $files )
        )"""
    params = {"files": [str(p) for p in parquets]}
    con.execute(query, params)


def get_all_contract_ids(con: DuckDBPyConnection) -> set[int]:
    query = "SELECT DISTINCT contract_id FROM raw_bidders"
    records = con.execute(query).fetchall()
    return {row[0] for row in records}


def delete_contract_ids(con: DuckDBPyConnection, contract_ids: set[int]) -> None:
    query = f"DELETE FROM raw_bidders WHERE contract_id IN {tuple(contract_ids)}"
    con.execute(query)
    con.commit()
