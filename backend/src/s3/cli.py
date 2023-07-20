import click

from src.s3.rclone import sync_from_s3, sync_to_s3
from src.settings import Settings


@click.group(help="Manage s3 buckets")
def s3() -> None:
    pass


@s3.command()
def sync_prod_to_s3() -> None:
    """Syncs local prod_sync_dir to prod_bucket"""
    settings = Settings()
    sync_to_s3(
        settings.rclone_remote,
        settings.prod_bucket,
        settings.prod_sync_dir,
    )


@s3.command()
def sync_dev_to_s3() -> None:
    """Syncs local dev_sync_dir to dev_bucket"""
    settings = Settings()
    sync_to_s3(
        settings.rclone_remote,
        settings.dev_bucket,
        settings.dev_sync_dir,
    )


@s3.command()
def sync_dev_from_s3() -> None:
    """Syncs dev_bucket to local dev_sync_dir"""
    settings = Settings()
    sync_from_s3(
        settings.rclone_remote,
        settings.dev_bucket,
        settings.dev_sync_dir,
    )
