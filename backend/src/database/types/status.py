from enum import StrEnum, auto

from duckdb import DuckDBPyConnection


class Status(StrEnum):
    NOT_RUN = "not run"
    COMPLETE = auto()
    FAILED = auto()


def create_status_type(con: DuckDBPyConnection) -> None:
    query = "CREATE TYPE status AS ENUM ('not run', 'complete', 'failed')"
    con.execute(query)
