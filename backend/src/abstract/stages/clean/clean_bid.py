from pathlib import Path

import polars as pl

from src.abstract.stages.clean.validate import (
    ValidationError,
    validate_columns,
    validate_no_missing_values,
)
from src.settings import Settings


def _cast_monitary_to_cents(s: pl.Series) -> pl.Series:
    """Cast a monitary string to int cents. Example: '$10.43' -> 1043"""
    return (
        s.str.strip()
        .str.replace_all("\\$", "")
        .str.replace_all(",", "")
        .cast(pl.Float32)
        * 100
    ).cast(pl.Int64)


def _validate_input_df(df: pl.DataFrame) -> None:
    """Raises a ValidationError if the provided DataFrame does pass validation checks."""
    required = {
        "ContractId",
        "SectionDescription",
        "LineNumber",
        "ItemNumber",
        "ItemDescription",
        "Quantity",
        "UnitName",
        "Engineers (Unit Price)",
    }
    validate_columns(df, required)


def _validate_output_df(df: pl.DataFrame) -> None:
    """Raises a ValidationError if the provided DataFrame does pass validation checks."""
    validate_no_missing_values(df)


def _clean_bid(csv: Path) -> pl.DataFrame:
    # Read all values as pl.Utf8 with infer_schema_length=0
    # Explicitly cast each non-string column in the next step
    df = pl.read_csv(csv, infer_schema_length=0)
    _validate_input_df(df)

    df_clean = df.select(
        [
            pl.col("ContractId").cast(pl.Int64).alias("contract_id"),
            pl.col("SectionDescription").str.strip().alias("section_description"),
            pl.col("LineNumber").cast(pl.Int64).alias("line_number"),
            pl.col("ItemNumber").str.slice(offset=0, length=4).alias("spec_code"),
            pl.col("ItemNumber").str.slice(offset=4, length=3).alias("unit_code"),
            pl.col("ItemNumber").str.slice(offset=8, length=5).alias("item_code"),
            pl.col("ItemDescription")
            .str.strip()
            .str.replace_all("''", '"')
            .alias("item_long_description"),
            pl.col("Quantity").cast(pl.Float32).alias("quantity"),
            pl.col("UnitName").str.strip().alias("unit_name"),
            pl.col("^*(Unit Price).+$").map(_cast_monitary_to_cents),
        ]
    )

    df_melt = df_clean.melt(
        id_vars=[
            "contract_id",
            "section_description",
            "line_number",
            "spec_code",
            "unit_code",
            "item_code",
            "item_long_description",
            "quantity",
            "unit_name",
        ],
        variable_name="bidder_name",
        value_name="unit_price_cents",
    )

    df_output = df_melt.select(
        [
            pl.all().exclude("bidder_name"),
            pl.col("bidder_name").str.replace("\\(Unit Price\\)", "").str.strip(),
        ]
    )
    _validate_output_df(df_output)
    return df_output


def clean_bid_csv(settings: Settings, contract_id: int) -> None:
    """Creates a cleaned CSV from a bid subtable CSV"""
    csv = settings.split_abstract_dir / f"{contract_id}_bid.csv"
    parquet = settings.clean_abstract_dir / f"{contract_id}_bid.parquet"

    try:
        df = _clean_bid(csv)
        # Write to parquet so that type casts are presevered
        df.write_parquet(parquet)
    except ValidationError as e:
        raise ValidationError(
            f"Failed to clean {csv.name} with message: {e.args[0]}"
        ) from e
