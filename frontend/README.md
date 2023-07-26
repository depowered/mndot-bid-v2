<div align="center">

# mndotbidprices.com

*Sveltekit + DuckDB-WASM = Lightning fast dashboard*

</div>

## Introduction

A Sveltekit application that uses a <a href="https://duckdb.org/docs/api/wasm/overview" target="_blank">web assembly build of DuckDB</a> to power analytical queries in the browser. All results, including search and bid data statistics, are computed in the browser using the DuckDB-WASM engine. Queries are executed at C-like speeds, returning results in tens of milliseconds with zero network latency.

The application is based on a combination of the <a href="https://github.com/shinokada/flowbite-svelte-starter" target="_blank">Flowbite-Svelte Starter</a> and the <a href="https://github.com/duckdb-wasm-examples/sveltekit-typescript/tree/main" target="_blank">SvelteKit-Typescript DuckDB-WASM demo</a>.

## Installation

Make sure you have <a href="https://nodejs.org/en/download" target="_blank">`node`</a> (Version `16` or later) installed.

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
