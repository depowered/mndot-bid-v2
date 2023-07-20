# Sveltekit + duckdb-WASM = Lightning fast dashboard

A Sveltekit application that uses a [web assembly build of duckdb](https://duckdb.org/docs/api/wasm/overview) to power analytical queries in the browser. All results, including search and bid data statistics, are computed in the browser using the duckdb-WASM engine allowing queries to be returned in tens of milliseconds with no network latency.

## Installation

Make sure you have [`node`](https://nodejs.org/en/download) (Version `16` or later) installed.

```bash
# Clone the repository
git clone https://github.com/depowered/mndot-bid-v2.git

# Enter the frontend directory
cd mndot-bid-v2/frontend

# Install the frontend dependencies
npm i

# Run the development server
npm run dev
```

The development server will be hosted at [localhost:5173](http://localhost:5173/). The public bucket that serves the source data for the dashboard accepts CORS requests from that address, allowing development builds to operate with production data.
