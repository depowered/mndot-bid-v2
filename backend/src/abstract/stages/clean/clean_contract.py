from pathlib import Path

import polars as pl

from src.abstract.stages.clean.validate import (
    ValidationError,
    validate_columns,
    validate_no_missing_values,
)
from src.settings import Settings


def _validate_input_df(df: pl.DataFrame) -> None:
    """Raises a ValidationError if the provided DataFrame does pass validation checks."""
    required = {
        "Contract Id",
        "Letting Date",
        "Job Description",
        "SP Number",
        "District",
        "County",
    }
    validate_columns(df, required)


def _validate_output_df(df: pl.DataFrame) -> None:
    """Raises a ValidationError if the provided DataFrame does pass validation checks."""
    validate_no_missing_values(df)


def _clean_contract(csv: Path) -> pl.DataFrame:
    # Read all values as pl.Utf8 with infer_schema_length=0
    # Explicitly cast each non-string column in the next step
    df = pl.read_csv(csv, infer_schema_length=0)
    _validate_input_df(df)

    df_clean = df.select(
        [
            pl.col("Contract Id").cast(pl.Int64).alias("contract_id"),
            pl.col("Letting Date")
            .str.strptime(pl.Date, format="%m/%d/%Y")
            .alias("letting_date"),
            pl.col("Job Description")
            .str.strip()
            .str.to_uppercase()
            .alias("job_description"),
            pl.col("SP Number").str.strip().alias("sp_number"),
            pl.col("District").str.strip().str.to_uppercase().alias("district"),
            pl.col("County").str.strip().str.to_uppercase().alias("county"),
        ]
    )
    _validate_output_df(df_clean)
    return df_clean


def clean_contract_csv(settings: Settings, contract_id: int) -> None:
    """Creates a cleaned CSV from a bid subtable CSV"""
    csv = settings.split_abstract_dir / f"{contract_id}_contract.csv"
    parquet = settings.clean_abstract_dir / f"{contract_id}_contract.parquet"

    try:
        df = _clean_contract(csv)
        # Write to parquet so that type casts are presevered
        df.write_parquet(parquet)
    except ValidationError as e:
        raise ValidationError(
            f"Failed to clean {csv.name} with message: {e.args[0]}"
        ) from e
    except pl.ComputeError as e:
        raise ValidationError(e.args[0]) from e
