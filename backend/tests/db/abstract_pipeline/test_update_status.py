from src.database.tables import abstract_pipeline
from tests.db.mock_db import DuckDBPyConnection, mock_con

Record = tuple[int, str, str, str, str]


def test_update_status_download(mock_con: DuckDBPyConnection):
    abstract_pipeline.update_status(
        con=mock_con,
        contract_id=10,
        stage=abstract_pipeline.Stage.DOWNLOAD,
        status=abstract_pipeline.Status.FAILED,
    )
    record: Record = mock_con.sql(
        "SELECT * FROM abstract_pipeline WHERE contract_id=10"
    ).fetchone()  # pyright: ignore
    assert record == (10, "failed", "complete", "complete", "complete")


def test_update_status_split(mock_con: DuckDBPyConnection):
    abstract_pipeline.update_status(
        con=mock_con,
        contract_id=10,
        stage=abstract_pipeline.Stage.SPLIT,
        status=abstract_pipeline.Status.FAILED,
    )
    record: Record = mock_con.sql(
        "SELECT * FROM abstract_pipeline WHERE contract_id=10"
    ).fetchone()  # pyright: ignore
    assert record == (10, "complete", "failed", "complete", "complete")


def test_update_status_clean(mock_con: DuckDBPyConnection):
    abstract_pipeline.update_status(
        con=mock_con,
        contract_id=10,
        stage=abstract_pipeline.Stage.CLEAN,
        status=abstract_pipeline.Status.FAILED,
    )
    record: Record = mock_con.sql(
        "SELECT * FROM abstract_pipeline WHERE contract_id=10"
    ).fetchone()  # pyright: ignore
    assert record == (10, "complete", "complete", "failed", "complete")
