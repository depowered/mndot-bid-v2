from pathlib import Path

from pydantic import BaseSettings, Field, HttpUrl

PROJECT_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    log_dir: Path = PROJECT_DIR / "logs/"
    data_dir: Path = PROJECT_DIR / "data/"

    # Database
    db: Path = data_dir / "raw-datastore.duckdb"
    db_dump_dir: Path = data_dir / "db_dump/"

    # Abstract processing
    raw_abstract_dir: Path = data_dir / "raw/abstracts/"
    split_abstract_dir: Path = data_dir / "interim/split_abstracts/"
    clean_abstract_dir: Path = data_dir / "interim/clean_abstracts/"
    mndot_abstracts_app: HttpUrl = Field(
        default="https://transport.dot.state.mn.us/PostLetting/Abstract.aspx"
    )
    download_abstract_url: HttpUrl = Field(
        default="https://transport.dot.state.mn.us/PostLetting/abstractCSV.aspx"
    )

    # Item list processing
    raw_item_list_dir: Path = data_dir / "raw/item_lists/"
    clean_item_list_dir: Path = data_dir / "interim/clean_item_lists/"
    download_item_list_url: HttpUrl = Field(
        default="https://transport.dot.state.mn.us/Reference/refItem.aspx"
    )

    # Data Build Tool (dbt)
    dbt_source_dir: Path = data_dir / "interim/dbt/source/"
