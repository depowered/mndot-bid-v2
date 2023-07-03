from pathlib import Path

import polars as pl

from src.item.stages.clean.validate import (
    ValidationError,
    validate_columns,
    validate_no_missing_values,
)
from src.settings import Settings


def _validate_input_df(df: pl.DataFrame) -> None:
    """Raises a ValidationError if the provided DataFrame does pass validation checks."""
    required = {
        "Item Number",
        "Short Description",
        "Long Description",
        "Unit Name",
        "Plan Unit Description",
        "Spec Year",
    }
    validate_columns(df, required)


def _validate_output_df(df: pl.DataFrame) -> None:
    """Raises a ValidationError if the provided DataFrame does pass validation checks."""
    validate_no_missing_values(df)


def _clean_item_list(csv: Path) -> pl.DataFrame:
    # Read all values as pl.Utf8 with infer_schema_length=0
    # Explicitly cast each non-string column in the next step
    df = pl.read_csv(csv, infer_schema_length=0)
    _validate_input_df(df)

    df_clean = df.select(
        [
            pl.col("Item Number").str.slice(offset=0, length=4).alias("spec_code"),
            pl.col("Item Number").str.slice(offset=5, length=3).alias("unit_code"),
            pl.col("Item Number").str.slice(offset=9, length=5).alias("item_code"),
            pl.col("Short Description")
            .str.strip()
            .str.replace_all(";", ",")
            .alias("short_description"),
            pl.col("Long Description")
            .str.strip()
            .str.replace_all(";", ",")
            .alias("long_description"),
            pl.col("Unit Name").str.strip().alias("unit_name"),
            pl.col("Plan Unit Description").str.strip().alias("plan_unit_description"),
            pl.col("Spec Year").cast(pl.Int64).add(2000).alias("spec_year"),
        ]
    )
    _validate_output_df(df_clean)
    return df_clean


def clean_item_list_csv(settings: Settings, year: int) -> None:
    """Creates a cleaned parquet from a raw item list CSV"""
    csv = settings.raw_item_list_dir / f"item_list_{year}.csv"
    parquet = settings.clean_item_list_dir / f"item_list_{year}.parquet"

    settings.clean_item_list_dir.mkdir(parents=True, exist_ok=True)
    try:
        df = _clean_item_list(csv)
        # Write to parquet so that type casts are presevered
        df.write_parquet(parquet)
    except ValidationError as e:
        raise ValidationError(
            f"Failed to clean {csv.name} with message: {e.args[0]}"
        ) from e
