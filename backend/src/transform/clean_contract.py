from pathlib import Path

import polars as pl

from src.settings import Settings


def clean_contract(csv: Path) -> pl.DataFrame:
    df = pl.read_csv(csv, try_parse_dates=False)
    exprs = [
        pl.col("Contract Id").cast(int).alias("contract_id"),
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
    return df.select(exprs)


if __name__ == "__main__":
    settings = Settings()
    contract_id = 210120
    filename = f"{contract_id}_contract.csv"
    input = settings.split_abstract_dir / filename
    df = clean_contract(input).head()
    print(df.head())
    output = settings.clean_abstract_dir / filename
    df.write_csv(output)
