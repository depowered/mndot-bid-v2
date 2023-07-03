import click

from src.abstract.cli import abstract
from src.database.cli import database
from src.item.cli import item


@click.group(help="Run data pipeline processes")
def cli() -> None:
    pass


cli.add_command(database)
cli.add_command(abstract)
cli.add_command(item)

if __name__ == "__main__":
    cli()
