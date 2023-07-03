import click

from src.abstract.pipeline import pipeline
from src.abstract.stages import clean, download, load, scrape, split
from src.database import db
from src.database.tables import abstract_pipeline
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
    if not scrape.done():
        scrape.run(settings, year)


@abstract.command()
def run_download() -> None:
    """Runs the download stage"""
    settings = Settings()
    if not download.done():
        download.run(settings)


@abstract.command()
def run_split() -> None:
    """Runs the split stage"""
    settings = Settings()
    if not split.done():
        split.run(settings)


@abstract.command()
def run_clean() -> None:
    """Runs the clean stage"""
    settings = Settings()
    if not clean.done():
        clean.run(settings)


@abstract.command()
def run_load() -> None:
    """Runs the load stage"""
    settings = Settings()
    if not load.done():
        load.run(settings)


@abstract.command()
@click.option(
    "--download",
    is_flag=True,
    show_default=True,
    default=False,
    help="Reset download stage",
)
@click.option(
    "--split",
    is_flag=True,
    show_default=True,
    default=False,
    help="Reset split stage",
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
    stages = []
    stages.append(abstract_pipeline.Stage.DOWNLOAD) if download else None
    stages.append(abstract_pipeline.Stage.SPLIT) if split else None
    stages.append(abstract_pipeline.Stage.CLEAN) if clean else None
    stages.append(abstract_pipeline.Stage.LOAD) if load else None
    if not stages:
        click.echo("No stages selected. See --help for options.")
        return
    abstract_pipeline.reset_stages(db.get_db_con(), stages)
