import click

from src.item.pipeline import pipeline
from src.item.stages import clean, download, load, scrape
from src.settings import Settings


@click.group(help="Item list processing commands")
def item() -> None:
    pass


@item.command()
@click.option("--year", type=int, required=True, help="Specification year")
def run_pipeline(year: int) -> None:
    """Runs the processing pipeline"""
    settings = Settings()
    pipeline(settings, year)


@item.command()
@click.option("--year", type=int, required=True, help="Specification year")
def run_scrape(year: int) -> None:
    """Runs the scrape stage"""
    settings = Settings()
    scrape.run(settings, year)


@item.command()
def run_download() -> None:
    """Runs the download stage"""
    settings = Settings()
    if not download.done():
        download.run(settings)


@item.command()
def run_clean() -> None:
    """Runs the clean stage"""
    settings = Settings()
    if not clean.done():
        clean.run(settings)


@item.command()
def run_load() -> None:
    """Runs the load stage"""
    settings = Settings()
    if not load.done():
        load.run(settings)


@item.command()
@click.option(
    "--download",
    is_flag=True,
    show_default=True,
    default=False,
    help="Reset download stage",
)
@click.option(
    "--clean",
    is_flag=True,
    show_default=True,
    default=False,
    help="Reset clean stage",
)
@click.option(
    "--load",
    is_flag=True,
    show_default=True,
    default=False,
    help="Reset load stage",
)
def reset_stages(download: bool, split: bool, clean: bool, load: bool) -> None:
    """Sets all records in provided stages to 'not run'"""
    pass
