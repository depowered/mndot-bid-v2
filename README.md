<div align="center">

# [mndotbidprices.com](https://mndotbidprices.com)

*An analytics dashboard application for exploring construction bids on Minnesota Department of Transportation (MnDOT) projects.*

[![item search preview](static/item-search-preview.png)](https://mndotbidprices.com)
</div>
## Introduction

Estimating the cost of a proposed construction project is often a difficult task for engineers. The factors impacting the cost of each unit of work are many and difficult to fully account for. Engineers often rely on cost data from past projects to inform their estimates. Sources such as MnDOT's own [Average Bid Price](https://edocs-public.dot.state.mn.us/edocs_public/DMResultSet/Urlsearch?columns=docnumber,docname,app_id&folderid=28521650) documents help with this, but often leave the user wanting for additional detail and recency.

This dashboard provides those more detailed and recent insights by scraping data from individual [awarded contract abstracts](https://www.dot.state.mn.us/bidlet/abstract.html) and providing summary statistics computed from that data.

## Usage

A hosted version of the dashboard is available at [mndotbidprices.com](https://mndotbidprices.com). See the dashboard's *Usage* section for detailed instructions for operating the application.

## Installation

### Clone the project

```bash
# Clone the repository
git clone https://github.com/depowered/mndot-bid-v2.git
```

### Frontend
Make sure you have [`node`](https://nodejs.org/en/download) (Version `16` or later) installed.

```bash
# Enter the frontend directory
cd mndot-bid-v2/frontend

# Install the frontend dependencies
npm i

# Run the development server
npm run dev
```

The development server will be hosted at [localhost:5173](http://localhost:5173/). The public bucket that serves the source data from the dashboard accepts `GET` & `HEAD` CORS requests from this host and port, allowing development builds to operate with production data.

### Backend

Make sure you have [`docker`](https://docs.docker.com/get-docker/) installed.

```bash
# Enter the backend directory
cd mndot-bid-v2/backend

# Build the docker image with the tag mndot-bid
docker build --tag mndot-bid .

# Run an interactive shell within the container
# The volume option (`-v`) binds the local data directory to the 
# data directory inside the container. This persists data artifacts
# locally between image runs.
docker run \
    -v ./data:/opt/mndot_bid/data \
    -it mndot-bid-prod
```

See the backend [README](backend/README.md) for instructions to setup and run data pipelines.

## [License](LICENSE)

MIT &copy; [Devin Power](https://github.com/depowered)