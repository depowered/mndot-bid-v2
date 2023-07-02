import re
from dataclasses import dataclass
from pathlib import Path

from src.settings import Settings


class SplitError(BaseException):
    pass


@dataclass(slots=True)
class Subtable:
    name: str
    content: str


def _split_abstract_into_subtables(content: str) -> list[Subtable]:
    """Splits the csv data by blank lines to divide into its three subtables."""
    blank_line_regex = r"(?:\r?\n){2,}"
    split = re.split(pattern=blank_line_regex, string=content)

    if len(split) != 3:
        raise SplitError()
    contract_content, bid_content, bidder_content = split

    return [
        Subtable("contract", contract_content),
        Subtable("bid", bid_content),
        Subtable("bidder", bidder_content),
    ]


def _write_subtable_csv(output_dir: Path, contract_id: int, subtable: Subtable) -> None:
    """Write the content of a subtable to a CSV file."""
    csv = output_dir / f"{contract_id}_{subtable.name}.csv"
    csv.write_text(data=subtable.content)


def split_abstract_csv(settings: Settings, contract_id: int) -> None:
    """Splits raw abstract CSVs into individual CSVs for each subtable."""
    input_dir = settings.raw_abstract_dir
    output_dir = settings.split_abstract_dir
    csv = input_dir / f"{contract_id}.csv"

    try:
        subtables = _split_abstract_into_subtables(csv.read_text())
    except SplitError as e:
        raise SplitError(f"Failed to split abstract: {csv.name}") from e

    for subtable in subtables:
        _write_subtable_csv(output_dir, contract_id, subtable)
