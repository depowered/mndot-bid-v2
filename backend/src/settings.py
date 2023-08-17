from pathlib import Path

from pydantic import BaseSettings

PROJECT_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    log_dir: Path = PROJECT_DIR / "logs/"
    data_dir: Path = PROJECT_DIR / "data/"

    # Database
    @property
    def db(self) -> Path:
        return self.data_dir / "clean_datastore.duckdb"

    # Abstract processing
    @property
    def raw_abstract_dir(self) -> Path:
        return self.data_dir / "raw/abstracts/"

    @property
    def split_abstract_dir(self) -> Path:
        return self.data_dir / "interim/split_abstracts/"

    @property
    def clean_abstract_dir(self) -> Path:
        return self.data_dir / "interim/clean_abstracts/"

    mndot_abstracts_app: str = (
        "https://transport.dot.state.mn.us/PostLetting/Abstract.aspx"
    )

    download_abstract_url: str = (
        "https://transport.dot.state.mn.us/PostLetting/abstractCSV.aspx"
    )

    # Item list processing
    @property
    def raw_item_list_dir(self) -> Path:
        return self.data_dir / "raw/item_lists/"

    @property
    def clean_item_list_dir(self) -> Path:
        return self.data_dir / "interim/clean_item_lists/"

    download_item_list_url: str = (
        "https://transport.dot.state.mn.us/Reference/refItem.aspx"
    )

    # Data Build Tool (dbt)
    dbt_project_dir: Path = PROJECT_DIR / "dbt/mndot_bid/"

    @property
    def dbt_source_dir(self) -> Path:
        return self.data_dir / "interim/dbt_source/"

    # S3
    rclone_remote: str = "mndotbids3"

    dev_bucket: str = "mndot-bid-dev"

    @property
    def dev_sync_dir(self) -> Path:
        """Directory to sync to and from the dev_bucket"""
        return self.data_dir

    prod_bucket: str = "mndot-bid"

    @property
    def prod_sync_dir(self) -> Path:
        """Directory to sync to and from the prod_bucket"""
        return self.data_dir / "processed/"
