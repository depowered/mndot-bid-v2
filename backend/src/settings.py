from pathlib import Path

from pydantic import BaseSettings

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data/"


class Settings(BaseSettings):
    data_dir: Path = DATA_DIR
    raw_abstract_dir = data_dir / "raw/abstracts/"

    mndot_abstracts_app: str = (
        "https://transport.dot.state.mn.us/PostLetting/Abstract.aspx"
    )
    download_abstract_url: str = (
        "https://transport.dot.state.mn.us/PostLetting/abstractCSV.aspx"
    )
