# Build Production Backend

The following describes how to setup a container that is fully configured to maintain production data via syncing to and from S3 buckets.

**REQUIRES:**

- S3 compliant object storage provider with two buckets: `mndot-bid` and `mndot-bid-dev`
- Credentials with read & write access to the buckets

## Build create volumes and build container

```bash
# Create volumes to store the project data, rclone configuration, and logs
docker volume create mndot-bid-data
docker volume create mndot-bid-config
docker volume create mndot-bid-logs

# Build the docker image
docker build --tag mndot-bid-cli .
```

## Initial Setup

```bash
# Run the container in an interactive session
docker run \
    -v mndot-bid-data:/opt/mndot_bid/data \
    -v mndot-bid-config:/root/.config/rclone/ \
    -v mndot-bid-logs:/opt/mndot_bid/logs \
    -it mndot-bid-cli

# Configure rclone via the interactive terminal interface
# Create a remote named 'mndotbids3' with credentials that
# has read & write access to both buckets noted above
rclone config

# Download data in the 'mndot-bid-dev' to the docker data volume
mndot-bid-cli s3 sync-dev-from-s3

# Run the process to update production parquets
./scripts/update_prod_parquets.sh

# If all went well, exit the container
exit
```

## Maintain Production Parquets

```bash
# Run the container with the update production parquets as the startup command
docker run \
    -v mndot-bid-data:/opt/mndot_bid/data \
    -v mndot-bid-config:/root/.config/rclone/ \
    -v mndot-bid-logs:/opt/mndot_bid/logs \
    mndot-bid-cli \
    /opt/mndot_bid/scripts/update_prod_parquets.sh
```
