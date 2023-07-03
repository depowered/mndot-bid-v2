import click

from src.abstract.cli import abstract
from src.database.cli import database
from src.item.cli import item
from src.logging import configure_logging, log_command


@click.group(help="Run data pipeline processes")
def cli() -> None:
    configure_logging()
    log_command()


cli.add_command(database)
cli.add_command(abstract)
cli.add_command(item)

if __name__ == "__main__":
    cli()
