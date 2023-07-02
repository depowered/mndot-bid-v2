from src.database import abstract_pipeline
from tests.db.mock_db import mock_con


def test_insert_new_records(mock_con):
    contract_ids = [40, 50]
    abstract_pipeline.insert_new_records(mock_con, contract_ids)
    count = mock_con.sql("SELECT count(*) FROM abstract_pipeline;").fetchone()[0]
    assert count == 5

    record = mock_con.sql(
        "SELECT * FROM abstract_pipeline WHERE contract_id=50"
    ).fetchone()
    assert record == (50, "not run", "not run", "not run")


def test_insert_new_records_existing(mock_con):
    contract_ids = [10, 20]  # These already exist; insert should be ignored
    abstract_pipeline.insert_new_records(mock_con, contract_ids)
    count = mock_con.sql("SELECT count(*) FROM abstract_pipeline").fetchone()[0]
    assert count == 3
