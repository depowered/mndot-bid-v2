from src.database.tables import abstract_pipeline
from tests.db.mock_db import DuckDBPyConnection, mock_con


def test_get_ids_with_status_not_run(mock_con: DuckDBPyConnection):
    contract_ids = abstract_pipeline.get_ids_with_status(
        con=mock_con,
        stage=abstract_pipeline.Stage.DOWNLOAD,
        status=abstract_pipeline.Status.NOT_RUN,
    )
    assert len(contract_ids) == 1
    assert contract_ids == {30}


def test_get_ids_with_status_complete(mock_con: DuckDBPyConnection):
    contract_ids = abstract_pipeline.get_ids_with_status(
        con=mock_con,
        stage=abstract_pipeline.Stage.DOWNLOAD,
        status=abstract_pipeline.Status.COMPLETE,
    )
    assert len(contract_ids) == 2
    assert contract_ids == {10, 20}


def test_get_ids_with_status_failed(mock_con: DuckDBPyConnection):
    contract_ids = abstract_pipeline.get_ids_with_status(
        con=mock_con,
        stage=abstract_pipeline.Stage.SPLIT,
        status=abstract_pipeline.Status.FAILED,
    )
    assert len(contract_ids) == 1
    assert contract_ids == {20}
