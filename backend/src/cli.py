import click

from src.extract.cli import download_abstracts


@click.group(help="Run data pipeline processes")
def cli() -> None:
    pass


cli.add_command(download_abstracts)

if __name__ == "__main__":
    cli()
