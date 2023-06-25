from pathlib import Path

from pydantic import BaseSettings, HttpUrl

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data/"


class Settings(BaseSettings):
    data_dir: Path = DATA_DIR
    raw_abstract_dir = data_dir / "raw/abstracts/"
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
