from duckdb import DuckDBPyConnection

from src.database import raw_bidders, raw_bids, raw_contracts
from src.settings import Settings


def load_raw_contracts(
    con: DuckDBPyConnection, settings: Settings, contract_ids: set[int]
) -> None:
    parquets = {
        settings.clean_abstract_dir / f"{id}_contract.parquet" for id in contract_ids
    }
    raw_contracts.create_or_replace_table(con, parquets)


def load_raw_bids(
    con: DuckDBPyConnection, settings: Settings, contract_ids: set[int]
) -> None:
    parquets = {
        settings.clean_abstract_dir / f"{id}_bid.parquet" for id in contract_ids
    }
    raw_bids.create_or_replace_table(con, parquets)


def load_raw_bidders(
    con: DuckDBPyConnection, settings: Settings, contract_ids: set[int]
) -> None:
    parquets = {
        settings.clean_abstract_dir / f"{id}_bidder.parquet" for id in contract_ids
    }
    raw_bidders.create_or_replace_table(con, parquets)
