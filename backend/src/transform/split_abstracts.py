import re
from enum import StrEnum, auto
from functools import partial
from pathlib import Path

from loguru import logger

from src.settings import Settings


class Subtable(StrEnum):
    CONTRACT = auto()
    BID = auto()
    BIDDER = auto()


def _already_split(settings: Settings) -> set[Path]:
    split_csvs = settings.split_abstract_dir.glob("*.csv")
    split_ids = {int(f.stem[:6]) for f in split_csvs}
    return {settings.raw_abstract_dir / f"{id}.csv" for id in split_ids}


def _split_abstract_csv(csv: Path) -> list[str]:
    """Splits the csv data by blank lines to divide into its three subtables."""
    with open(csv, "r") as f:
        content = f.read()
    blank_line_regex = r"(?:\r?\n){2,}"
    subtables = re.split(blank_line_regex, content)

    if len(subtables) != 3:
        raise ValueError(f"{csv.name} did not split into 3 subtables.")

    return subtables


def _write_subtable_csv(
    output_dir: Path, contract_id: int, subtable: Subtable, content: str
) -> None:
    """Write the content of a subtable to a CSV file."""
    csv = output_dir / f"{contract_id}_{subtable}.csv"
    with open(csv, "w") as f:
        f.write(content)


def _handle_successful_split(
    output_dir: Path, contract_id: int, subtables: list[str]
) -> None:
    """Writes contract, bid, and bidder subtables to CSV files."""
    contract, bid, bidder = subtables
    write_csv = partial(
        _write_subtable_csv, output_dir=output_dir, contract_id=contract_id
    )
    write_csv(subtable=Subtable.CONTRACT, content=contract)
    write_csv(subtable=Subtable.BID, content=bid)
    write_csv(subtable=Subtable.BIDDER, content=bidder)


def _handle_failed_split(output_dir: Path, contract_id: int, error_msg: str) -> None:
    """Writes a file to the output directory named "{contract_id}_failed.csv.
    The presence of this file will prevent unsuccessful splits from being reattempted
    on subsequent runs."""
    csv = output_dir / f"{contract_id}_failed.csv"
    with open(csv, "w") as f:
        f.write(error_msg)


def split_abstract_csvs(settings: Settings) -> None:
    """Splits raw abstract CSVs into individual CSVs for each subtable."""
    abstracts = set(settings.raw_abstract_dir.glob("*.csv"))
    to_split = abstracts - _already_split(settings)

    count = len(to_split)
    if count < 1:
        logger.info("SPLIT: Found no abstracts to split")
        return
    logger.info(f"SPLIT: Found {count} abstracts to split")

    settings.split_abstract_dir.mkdir(parents=True, exist_ok=True)
    for idx, csv in enumerate(to_split):
        logger.info(
            f"SPLIT: Splitting {csv.name} into subtables ({idx + 1} of {count})"
        )
        contract_id = int(csv.stem)
        try:
            subtables = _split_abstract_csv(csv)
        except ValueError as e:
            _handle_failed_split(settings.split_abstract_dir, contract_id, e.args[0])
            logger.warning(f"SPLIT: Failed to split {csv.name}")
            continue
        _handle_successful_split(settings.split_abstract_dir, contract_id, subtables)
