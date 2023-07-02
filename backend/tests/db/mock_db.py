from pathlib import Path

import duckdb
import pytest
from duckdb import DuckDBPyConnection


@pytest.fixture()
def mock_con() -> DuckDBPyConnection:
    con = duckdb.connect(":memory:")
    query = (Path(__file__).resolve().parent / "mock_db.sql").read_text()
    con.execute(query)
    con.commit()
    return con
