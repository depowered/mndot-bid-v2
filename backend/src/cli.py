import click

from src.abstract.cli import abstract
from src.database.cli import database
from src.dbt.cli import dbt
from src.item.cli import item
from src.logging import configure_logging, log_command
from src.s3.cli import s3


@click.group(help="Run data pipeline processes")
def cli() -> None:
    configure_logging()
    log_command()


cli.add_command(database)
cli.add_command(abstract)
cli.add_command(item)
cli.add_command(s3)
cli.add_command(dbt)

if __name__ == "__main__":
    cli()
