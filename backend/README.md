<div align="center">

# mndot-bid-cli

*A command line interface (CLI) for orchestrating ETL pipelines that produce and publish data for the [mndotbidprices.com](https://mndotbidprices.com) analytical dashboard.*

</div>

```bash
Usage: mndot-bid-cli [OPTIONS] COMMAND [ARGS]...

Run data pipeline processes

Options:
--help  Show this message and exit.

Commands:
abstract  Abstract processing commands
database  Database management commands
dbt       dbt convenience commands
item      Item list processing commands
s3        Manage s3 buckets
```

## Installation

Make sure you have [`docker`](https://docs.docker.com/get-docker/) installed.

```bash
# Clone the repository
git clone https://github.com/depowered/mndot-bid-v2.git

# Enter the backend directory
cd mndot-bid-v2/backend

# Build the docker image with the tag mndot-bid-cli
docker build --tag mndot-bid-cli .

# Run an interactive shell within the container
# The volume option (`-v`) binds the local data directory to the 
# data directory inside the container. This persists data artifacts
# locally between image runs.
docker run \
    -v ./data:/opt/mndot_bid/data \
    -it mndot-bid-cli
```

## Usage

The following sections provide an overview of how to setup, create, and maintain production parquets used in the frontend dashboard.

### Initial Setup

To initialize the project, use the cli to create a database `clean_datastore.duckdb` for tracking and storing pipeline runs. Then ingest bid item lists and bid abstracts for the current year using the respective `run-pipeline` commands.

```bash
# Create an empty database: ./data/clean_datastore.duckdb
mndot-bid-cli database create

# Run ETL pipeline to ingest item lists
mndot-bid-cli item run-pipeline

# Run ETL pipeline to ingest abstracts for the current year
mndot-bid-cli abstract run-pipeline

# Additional years can be loaded by providing the --year option
mndot-bid-cli abstract run-pipeline --year 2022
```

### Create Production Parquets

Once data is loaded into the `clean_datastore.duckdb` database, it can be transformed further using dbt to produce the production parquets used in the frontend dashboard.

```bash
# Create production parquets and write to ./data/processed/
mndot-bid-cli dbt run

# Run tests to validate results
mndot-bid-cli dbt test
```

### Updating

The ETL pipelines track stage execution for each sourcefile to avoid unnecessary downloading and processing of data that is already present in the `clean_datastore.duckdb` database. This means that keeping the production parquets up-to-date is as simple as rerunning the abstract pipeline and dbt transformations.

```bash
# Download and process any newly published abstracts
mndot-bid-cli abstract run-pipeline

# Recreate and validate production parquets at ./data/processed/
mndot-bid-cli dbt run
mndot-bid-cli dbt test
```
