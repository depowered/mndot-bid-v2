from src.database.tables import abstract_pipeline
from tests.db.mock_db import DuckDBPyConnection, mock_con


def test_insert_new_records(mock_con: DuckDBPyConnection):
    contract_ids = {40, 50}
    abstract_pipeline.insert_new_records(mock_con, contract_ids)
    count: tuple[int] = mock_con.sql(
        "SELECT count(*) FROM abstract_pipeline;"
    ).fetchone()  # pyright: ignore
    assert count[0] == 5

    record: tuple[int, str, str, str, str] = mock_con.sql(
        "SELECT * FROM abstract_pipeline WHERE contract_id=50"
    ).fetchone()  # pyright: ignore
    assert record == (50, "not run", "not run", "not run", "not run")


def test_insert_new_records_existing(mock_con: DuckDBPyConnection):
    contract_ids = {10, 20}  # These already exist; insert should be ignored
    abstract_pipeline.insert_new_records(mock_con, contract_ids)
    count: tuple[int] = mock_con.sql(
        "SELECT count(*) FROM abstract_pipeline"
    ).fetchone()  # pyright: ignore
    assert count[0] == 3
