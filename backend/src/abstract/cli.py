import click

from src.abstract.pipeline import pipeline
from src.abstract.stages import download, scrape
from src.settings import Settings


@click.group(help="Abstract processing commands")
def abstract() -> None:
    pass


@abstract.command()
@click.option("--year", type=int, required=True, help="Bid opening year")
def run_pipeline(year: int) -> None:
    """Runs the processing pipeline"""
    settings = Settings()
    pipeline(settings, year)


@abstract.command()
@click.option("--year", type=int, required=True, help="Bid opening year")
def run_scrape(year: int) -> None:
    """Runs the scrape stage"""
    settings = Settings()
    scrape.run(settings, year)


@abstract.command()
def run_download() -> None:
    """Runs the download stage"""
    settings = Settings()
    if not download.done():
        download.run(settings)
