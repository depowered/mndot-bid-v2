from pathlib import Path

from pydantic_settings import BaseSettings

PROJECT_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    log_dir: Path = PROJECT_DIR / "logs/"
    data_dir: Path = PROJECT_DIR / "data/"

    # Database
    db: Path = data_dir / "clean_datastore.duckdb"

    # Abstract processing
    raw_abstract_dir: Path = data_dir / "raw/abstracts/"
    split_abstract_dir: Path = data_dir / "interim/split_abstracts/"
    clean_abstract_dir: Path = data_dir / "interim/clean_abstracts/"
    mndot_abstracts_app: str = (
        "https://transport.dot.state.mn.us/PostLetting/Abstract.aspx"
    )

    download_abstract_url: str = (
        "https://transport.dot.state.mn.us/PostLetting/abstractCSV.aspx"
    )

    # Item list processing
    raw_item_list_dir: Path = data_dir / "raw/item_lists/"
    clean_item_list_dir: Path = data_dir / "interim/clean_item_lists/"
    download_item_list_url: str = (
        "https://transport.dot.state.mn.us/Reference/refItem.aspx"
    )

    # Data Build Tool (dbt)
    dbt_project_dir: Path = PROJECT_DIR / "dbt/mndot_bid/"
    dbt_source_dir: Path = data_dir / "interim/dbt_source/"

    # S3
    # Create interactively with rclone cli
    rclone_config: Path = PROJECT_DIR / "rclone.conf"
    rclone_remote: str = "CloudflareR2"

    dev_bucket: str = "mndot-bid-dev"
    dev_sync_dir: Path = data_dir

    prod_bucket: str = "mndot-bid"
    prod_sync_dir: Path = data_dir / "processed/"
