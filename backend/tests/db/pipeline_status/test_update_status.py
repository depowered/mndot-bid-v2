from src.database import pipeline_status
from tests.db.mock_db import mock_con


def test_update_status_download(mock_con):
    pipeline_status.update_status(
        con=mock_con,
        contract_id=10,
        stage=pipeline_status.Stage.DOWNLOAD,
        status=pipeline_status.Status.FAILED,
    )
    record = mock_con.sql(
        "SELECT * FROM pipeline_status WHERE contract_id=10"
    ).fetchone()
    assert record == (10, "failed", "complete", "complete")


def test_update_status_split(mock_con):
    pipeline_status.update_status(
        con=mock_con,
        contract_id=10,
        stage=pipeline_status.Stage.SPLIT,
        status=pipeline_status.Status.FAILED,
    )
    record = mock_con.sql(
        "SELECT * FROM pipeline_status WHERE contract_id=10"
    ).fetchone()
    assert record == (10, "complete", "failed", "complete")


def test_update_status_clean(mock_con):
    pipeline_status.update_status(
        con=mock_con,
        contract_id=10,
        stage=pipeline_status.Stage.CLEAN,
        status=pipeline_status.Status.FAILED,
    )
    record = mock_con.sql(
        "SELECT * FROM pipeline_status WHERE contract_id=10"
    ).fetchone()
    assert record == (10, "complete", "complete", "failed")
