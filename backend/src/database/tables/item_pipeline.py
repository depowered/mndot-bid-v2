from enum import StrEnum

from duckdb import DuckDBPyConnection

from src.database.types.status import Status

__tablename__ = "item_pipeline"


class Stage(StrEnum):
    DOWNLOAD = "download_stage"
    CLEAN = "clean_stage"
    LOAD = "load_stage"


def create_table(con: DuckDBPyConnection) -> None:
    query = f"""
    CREATE TABLE {__tablename__} (
        spec_year INTEGER PRIMARY KEY,
        download_stage status DEFAULT 'not run',
        clean_stage status DEFAULT 'not run',
        load_stage status DEFAULT 'not run',
    )"""
    con.execute(query)


def insert_new_records(con: DuckDBPyConnection, spec_years: set[int]) -> None:
    query = f"INSERT OR IGNORE INTO {__tablename__} ( spec_year ) VALUES( ? )"
    params = [[year] for year in spec_years]
    con.executemany(query, params)
    con.commit()


def update_status(
    con: DuckDBPyConnection, spec_year: int, stage: Stage, status: Status
) -> None:
    query = f"""
        UPDATE {__tablename__}
        SET {stage} = $status
        WHERE spec_year = $spec_year
    """
    params = {"status": status, "spec_year": spec_year}
    con.execute(query, params)
    con.commit()


def reset_stages(con: DuckDBPyConnection, stages: list[Stage]) -> None:
    """Sets all records in provided stages to `Status.NOT_RUN`"""
    for stage in stages:
        query = f"UPDATE {__tablename__} SET {stage} = $status"
        params = {"status": Status.NOT_RUN}
        con.execute(query, params)
    con.commit()


def get_years_with_status(
    con: DuckDBPyConnection, stage: Stage, status: Status
) -> set[int]:
    query = f"SELECT spec_year FROM {__tablename__} WHERE {stage} = $status"
    params = {"status": status}
    records: list[tuple[int]] = con.execute(query, params).fetchall()  # pyright: ignore
    return {row[0] for row in records}
