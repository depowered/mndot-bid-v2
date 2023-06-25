import click

from src.extract.cli import download_abstracts, download_item_list


@click.group(help="Run data pipeline processes")
def cli() -> None:
    pass


cli.add_command(download_abstracts)
cli.add_command(download_item_list)

if __name__ == "__main__":
    cli()
