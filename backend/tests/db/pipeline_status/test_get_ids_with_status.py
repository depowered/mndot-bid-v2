from src.database import pipeline_status
from tests.db.mock_db import mock_con


def test_get_ids_with_status_not_run(mock_con):
    contract_ids = pipeline_status.get_ids_with_status(
        con=mock_con,
        stage=pipeline_status.Stage.DOWNLOAD,
        status=pipeline_status.Status.NOT_RUN,
    )
    assert len(contract_ids) == 1
    assert contract_ids == {30}


def test_get_ids_with_status_complete(mock_con):
    contract_ids = pipeline_status.get_ids_with_status(
        con=mock_con,
        stage=pipeline_status.Stage.DOWNLOAD,
        status=pipeline_status.Status.COMPLETE,
    )
    assert len(contract_ids) == 2
    assert contract_ids == {10, 20}


def test_get_ids_with_status_failed(mock_con):
    contract_ids = pipeline_status.get_ids_with_status(
        con=mock_con,
        stage=pipeline_status.Stage.SPLIT,
        status=pipeline_status.Status.FAILED,
    )
    assert len(contract_ids) == 1
    assert contract_ids == {20}
