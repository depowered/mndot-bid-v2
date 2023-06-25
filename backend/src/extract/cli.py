import click

from src.extract.download_abstracts import download_abstract_csvs
from src.extract.scrape_contract_ids import scrape_contract_ids
from src.settings import Settings


@click.command()
@click.option("--year", type=int, required=True, help="Bid opening year")
def download_abstracts(year: int) -> None:
    """Download all abstract CSVs for a given year"""
    settings = Settings()
    contract_ids = scrape_contract_ids(settings, year)
    download_abstract_csvs(settings, contract_ids)
