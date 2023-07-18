import os
from datetime import datetime
from subprocess import run

import click

from src.abstract.pipeline import pipeline
from src.production.s3 import list_bucket_objects, put_prod_parquets
from src.settings import Settings


@click.group(help="Create and publish production parquets")
def production() -> None:
    pass


@production.command()
def refresh() -> None:
    """Refreshes production parquets with the latest source data"""
    settings = Settings()
    pipeline(settings, datetime.now().year)
    os.chdir(settings.dbt_project_dir)
    run(["dbt", "run"])


@production.command()
def publish() -> None:
    """Pushes production parquets to object storage"""
    settings = Settings()
    put_prod_parquets(settings)


@production.command()
def list_objects() -> None:
    """Lists objects in s3 bucket"""
    settings = Settings()
    list_bucket_objects(settings)
