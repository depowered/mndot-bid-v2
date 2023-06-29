from src.database import pipeline_status
from tests.db.mock_db import mock_con


def test_insert_new_records(mock_con):
    contract_ids = [40, 50]
    pipeline_status.insert_new_records(mock_con, contract_ids)
    count = mock_con.sql("SELECT count(*) FROM pipeline_status;").fetchone()[0]
    assert count == 5

    record = mock_con.sql(
        "SELECT * FROM pipeline_status WHERE contract_id=50"
    ).fetchone()
    assert record == (50, "not run", "not run", "not run")


def test_insert_new_records_existing(mock_con):
    contract_ids = [10, 20]  # These already exist; insert should be ignored
    pipeline_status.insert_new_records(mock_con, contract_ids)
    count = mock_con.sql("SELECT count(*) FROM pipeline_status").fetchone()[0]
    assert count == 3
