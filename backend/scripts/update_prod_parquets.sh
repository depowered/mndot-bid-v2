#!/bin/bash

# Runs commands to update the parquets in the prod bucket with the latest source data
mndot-bid-cli item run-pipeline
mndot-bid-cli abstract run-pipeline
mndot-bid-cli dbt run
mndot-bid-cli s3 sync-dev-to-s3
mndot-bid-cli s3 sync-prod-to-s3