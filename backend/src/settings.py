from pathlib import Path

from pydantic import BaseSettings

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data/"


class Settings(BaseSettings):
    data_dir: Path = DATA_DIR
