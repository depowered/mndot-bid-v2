from enum import StrEnum

from duckdb import DuckDBPyConnection

from src.database.types.status import Status

tablename = "abstract_pipeline"


class Stage(StrEnum):
    DOWNLOAD = "download_stage"
    SPLIT = "split_stage"
    CLEAN = "clean_stage"
    LOAD = "load_stage"


def create_table(con: DuckDBPyConnection) -> None:
    query = f"""
    CREATE TABLE {tablename} (
        contract_id INTEGER PRIMARY KEY,
        download_stage status DEFAULT 'not run',
        split_stage status DEFAULT 'not run',
        clean_stage status DEFAULT 'not run',
        load_stage status DEFAULT 'not run',
    )"""
    con.execute(query)


def insert_new_records(con: DuckDBPyConnection, contract_ids: set[int]) -> None:
    query = f"INSERT OR IGNORE INTO {tablename} ( contract_id ) VALUES( ? )"
    params = [[id] for id in contract_ids]
    con.executemany(query, params)
    con.commit()


def update_status(
    con: DuckDBPyConnection, contract_id: int, stage: Stage, status: Status
) -> None:
    query = f"""
        UPDATE {tablename}
        SET {stage} = $status
        WHERE contract_id = $contract_id
    """
    params = {"status": status, "contract_id": contract_id}
    con.execute(query, params)
    con.commit()


def reset_stages(con: DuckDBPyConnection, stages: list[Stage]) -> None:
    """Sets all records in provided stages to `Status.NOT_RUN`"""
    for stage in stages:
        query = f"UPDATE {tablename} SET {stage} = $status"
        params = {"status": Status.NOT_RUN}
        con.execute(query, params)
    con.commit()


def get_ids_with_status(
    con: DuckDBPyConnection, stage: Stage, status: Status
) -> set[int]:
    query = f"SELECT contract_id FROM {tablename} WHERE {stage} = $status"
    params = {"status": status}
    records: list[tuple[int]] = con.execute(query, params).fetchall()  # pyright: ignore
    return {row[0] for row in records}
