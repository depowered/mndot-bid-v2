from pathlib import Path

import polars as pl

from src.settings import Settings


def cast_monitary_to_cents(s: pl.Series) -> pl.Series:
    """Cast a monitary string to int cents. Example: '$10.43' -> 1043"""
    clean = s.strip().replace("$", "").replace(",", "")
    return int(float(clean) * 100)


def clean_bidder(csv: Path, contract_id: int) -> pl.DataFrame:
    df = pl.read_csv(csv)
    df_clean = df.select(
        [
            pl.lit(contract_id).alias("contract_id"),
            pl.col("Bidder Number").cast(int).alias("bidder_id"),
            pl.col("Bidder Name").str.strip().alias("bidder_name"),
            pl.col("Bidder Amount")
            .apply(cast_monitary_to_cents)
            .alias("bid_total_cents"),
        ]
    )
    return df_clean


if __name__ == "__main__":
    settings = Settings()
    contract_id = 210120
    filename = f"{contract_id}_bidder.csv"
    input = settings.split_abstract_dir / filename
    df = clean_bidder(input, contract_id)
    print(df.head())
    output = settings.clean_abstract_dir / filename
    df.write_csv(output)
