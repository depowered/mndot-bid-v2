#!bin/sh

# Runs commands to update the parquets in the prod bucket with the latest source data
poetry run mndot-bid-cli item run-pipeline
poetry run mndot-bid-cli abstract run-pipeline
poetry run mndot-bid-cli dbt run
poetry run mndot-bid-cli s3 sync-dev-to-s3
poetry run mndot-bid-cli s3 sync-prod-to-s3