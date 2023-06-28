import click

from src.extract.cli import download_abstracts, download_item_list
from src.transform.cli import split_abstracts
from src.db.cli import database


@click.group(help="Run data pipeline processes")
def cli() -> None:
    pass


cli.add_command(download_abstracts)
cli.add_command(download_item_list)
cli.add_command(split_abstracts)
cli.add_command(database)

if __name__ == "__main__":
    cli()
