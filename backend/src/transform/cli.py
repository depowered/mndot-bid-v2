import click

from src.settings import Settings
from src.transform.split_abstracts import split_abstract_csvs


@click.command()
def split_abstracts() -> None:
    """Split all abstract CSVs into subtables"""
    settings = Settings()
    split_abstract_csvs(settings)
