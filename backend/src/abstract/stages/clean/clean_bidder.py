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
        "Bidder Number",
        "Bidder Name",
        "Bidder Amount",
    }
    validate_columns(df, required)


def _validate_output_df(df: pl.DataFrame) -> None:
    """Raises a ValidationError if the provided DataFrame does pass validation checks."""
    validate_no_missing_values(df)


def _clean_bidder(csv: Path, contract_id: int) -> pl.DataFrame:
    # Read all values as pl.Utf8 with infer_schema_length=0
    # Explicitly cast each non-string column in the next step
    df = pl.read_csv(csv, infer_schema_length=0)
    _validate_input_df(df)

    df_clean = df.select(
        [
            pl.lit(contract_id).alias("contract_id").cast(pl.Int64),
            pl.col("Bidder Number").cast(pl.Int64).alias("bidder_id"),
            pl.col("Bidder Name").str.strip().alias("bidder_name"),
            pl.col("Bidder Amount")
            .map(_cast_monitary_to_cents)
            .alias("bid_total_cents"),
        ]
    )
    _validate_output_df(df_clean)
    return df_clean


def clean_bidder_csv(settings: Settings, contract_id: int) -> None:
    """Creates a cleaned CSV from a bid subtable CSV"""
    csv = settings.split_abstract_dir / f"{contract_id}_bidder.csv"
    parquet = settings.clean_abstract_dir / f"{contract_id}_bidder.parquet"

    try:
        df = _clean_bidder(csv, contract_id)
        # Write to parquet so that type casts are presevered
        df.write_parquet(parquet)
    except ValidationError as e:
        raise ValidationError(
            f"Failed to clean {csv.name} with message: {e.args[0]}"
        ) from e
    except pl.ComputeError as e:
        raise ValidationError(e.args[0]) from e
