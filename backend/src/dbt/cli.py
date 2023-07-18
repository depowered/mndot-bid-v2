import os
import subprocess

import click

from src.settings import Settings


@click.group(help="dbt convenience commands")
def dbt() -> None:
    pass


@dbt.command()
def run() -> None:
    """Alias for `dbt run` from dbt project directory"""
    settings = Settings()
    os.chdir(settings.dbt_project_dir)
    subprocess.run(["dbt", "run"])


@dbt.command()
def test() -> None:
    """Alias for `dbt test` from dbt project directory"""
    settings = Settings()
    os.chdir(settings.dbt_project_dir)
    subprocess.run(["dbt", "test"])
