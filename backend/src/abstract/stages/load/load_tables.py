from duckdb import DuckDBPyConnection

from src.database.tables import clean_bidders, clean_bids, clean_contracts
from src.settings import Settings


def load_clean_contracts(
    con: DuckDBPyConnection, settings: Settings, contract_ids: set[int]
) -> None:
    parquets = {
        settings.clean_abstract_dir / f"{id}_contract.parquet" for id in contract_ids
    }
    clean_contracts.create_or_replace_table(con, parquets)


def load_clean_bids(
    con: DuckDBPyConnection, settings: Settings, contract_ids: set[int]
) -> None:
    parquets = {
        settings.clean_abstract_dir / f"{id}_bid.parquet" for id in contract_ids
    }
    clean_bids.create_or_replace_table(con, parquets)


def load_clean_bidders(
    con: DuckDBPyConnection, settings: Settings, contract_ids: set[int]
) -> None:
    parquets = {
        settings.clean_abstract_dir / f"{id}_bidder.parquet" for id in contract_ids
    }
    clean_bidders.create_or_replace_table(con, parquets)
