from pathlib import Path

from pydantic import BaseSettings, HttpUrl

PROJECT_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    data_dir: Path = PROJECT_DIR / "data/"
    db: Path = data_dir / "mndot-bid-dev.duckdb"

    raw_abstract_dir = data_dir / "raw/abstracts/"
    split_abstract_dir = data_dir / "interim/split_abstracts/"
    clean_abstract_dir = data_dir / "interim/clean_abstracts/"

    raw_item_list_dir = data_dir / "raw/item_lists/"

    mndot_abstracts_app: HttpUrl = (
        "https://transport.dot.state.mn.us/PostLetting/Abstract.aspx"
    )
    download_abstract_url: HttpUrl = (
        "https://transport.dot.state.mn.us/PostLetting/abstractCSV.aspx"
    )
    download_item_list_url: HttpUrl = (
        "https://transport.dot.state.mn.us/Reference/refItem.aspx"
    )
