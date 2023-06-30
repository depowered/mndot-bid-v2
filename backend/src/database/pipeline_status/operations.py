from duckdb import DuckDBPyConnection

from src.database.pipeline_status.enums import Stage, Status


def create_status_type(con: DuckDBPyConnection) -> None:
    query = "CREATE TYPE status AS ENUM ('not run', 'complete', 'failed')"
    con.execute(query)


def create_table(con: DuckDBPyConnection) -> None:
    query = """
    CREATE TABLE pipeline_status (
        contract_id INTEGER PRIMARY KEY,
        download_stage status DEFAULT 'not run',
        split_stage status DEFAULT 'not run',
        clean_stage status DEFAULT 'not run',
        load_stage status DEFAULT 'not run',
    )"""
    con.execute(query)


def insert_new_records(con: DuckDBPyConnection, contract_ids: list[int]) -> None:
    query = "INSERT OR IGNORE INTO pipeline_status( contract_id ) VALUES( ? )"
    params = [[id] for id in contract_ids]
    con.executemany(query, params)
    con.commit()


def update_status(
    con: DuckDBPyConnection, contract_id: int, stage: Stage, status: Status
) -> None:
    query = f"""
        UPDATE pipeline_status
        SET {stage} = $status
        WHERE contract_id = $contract_id
    """
    params = {"status": status, "contract_id": contract_id}
    con.execute(query, params)
    con.commit()


def get_ids_with_status(
    con: DuckDBPyConnection, stage: Stage, status: Status
) -> set[int]:
    query = f"SELECT contract_id FROM pipeline_status WHERE {stage} = $status"
    params = {"status": status}
    records = con.execute(query, params).fetchall()
    return {row[0] for row in records}
