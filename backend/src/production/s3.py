import boto3
from loguru import logger
from mypy_boto3_s3.service_resource import S3ServiceResource

from src.settings import Settings


def get_s3_client(settings: Settings) -> S3ServiceResource:
    return boto3.resource(
        "s3",
        endpoint_url=settings.endpoint_url,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


def list_bucket_objects(settings: Settings) -> None:
    s3: S3ServiceResource = get_s3_client(settings)
    bucket = s3.Bucket("mndot-bid")

    for item in bucket.objects.all():
        logger.info(
            f"Bucket: {bucket.name}, Object: {item.key}, Size: {item.size} bytes"
        )


def put_prod_parquets(settings: Settings) -> None:
    s3: S3ServiceResource = get_s3_client(settings)
    bucket = s3.Bucket("mndot-bid")

    prod_parquets = list(settings.prod_parquet_dir.glob("*.parquet"))
    for parquet in prod_parquets:
        logger.info(f"PUBLISH: Uploading {parquet.name} to {bucket.name} bucket")
        bucket.upload_file(str(parquet), parquet.name)
