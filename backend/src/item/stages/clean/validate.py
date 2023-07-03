import polars as pl


class ValidationError(BaseException):
    pass


def validate_columns(df: pl.DataFrame, required: set[str]) -> None:
    """Raises a ValidationError if the DataFrame does not contain the required columns."""
    in_df = {c.strip() for c in df.columns}
    missing = required - in_df
    if len(missing) != 0:
        raise ValidationError(f"Dataframe is missing columns: {missing}")


def validate_no_missing_values(df: pl.DataFrame) -> None:
    """Raises a ValidationError if the DataFrame contains any NULL values."""
    dropped = df.select(pl.all().drop_nulls().drop_nans())
    missing = df.shape[0] - dropped.shape[0]
    if missing != 0:
        raise ValidationError(f"Missing values in {missing} row(s)")
