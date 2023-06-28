from pathlib import Path

import polars as pl

from src.settings import Settings


def cast_monitary_to_cents(value: str | float) -> int:
    """Cast a monitary string to int cents. Example: '$10.43' -> 1043"""
    if isinstance(value, str):
        clean = value.strip().replace("$", "").replace(",", "")
        return int(float(clean) * 100)
    return int(value * 100)


def clean_bid(csv: Path) -> pl.DataFrame:
    df = pl.read_csv(csv)
    df_clean = df.select(
        [
            pl.col("ContractId").cast(int).alias("contract_id"),
            pl.col("SectionDescription").str.strip().alias("section_description"),
            pl.col("LineNumber").cast(int).alias("line_number"),
            pl.col("ItemNumber").str.slice(offset=0, length=4).alias("spec_code"),
            pl.col("ItemNumber").str.slice(offset=4, length=3).alias("unit_code"),
            pl.col("ItemNumber").str.slice(offset=8, length=5).alias("item_code"),
            pl.col("ItemDescription")
            .str.strip()
            .str.replace("''", '"')
            .alias("item_long_description"),
            pl.col("Quantity").cast(float).alias("quantity"),
            pl.col("UnitName").str.strip().alias("unit_name"),
            pl.col("^*(Unit Price).+$").apply(cast_monitary_to_cents),
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

    return df_melt.select(
        [
            pl.all().exclude("bidder_name"),
            pl.col("bidder_name").str.replace("\(Unit Price\)", "").str.strip(),
        ]
    )


if __name__ == "__main__":
    settings = Settings()
    contract_id = 210120
    filename = f"{contract_id}_bid.csv"
    input = settings.split_abstract_dir / filename
    df = clean_bid(input)
    print(df.head())
    output = settings.clean_abstract_dir / filename
    df.write_csv(output)
