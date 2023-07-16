import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import mvp_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
import duckdb_wasm_eh from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';

import type { AsyncDuckDB, AsyncDuckDBConnection } from '@duckdb/duckdb-wasm'

let db: AsyncDuckDB | null = null;

const BUCKET = 'https://r2.mndotbidprices.com'

const TABLES = {
  items: { tableName: 'prod_item_search', source: `${BUCKET}/prod_item_search.parquet` },
  bids: { tableName: 'prod_bids', source: `${BUCKET}/prod_bids.parquet` },
  weightedAvgByYear: { tableName: 'prod_item_weighted_avg_by_year', source: `${BUCKET}/prod_item_weighted_avg_by_year.parquet` }
}

// Setup and connect to the database

const initDB = async () => {
  if (db) {
    return db;  // Return existing db if already initialized
  }

  const MANUAL_BUNDLES: duckdb.DuckDBBundles = {
    mvp: {
      mainModule: duckdb_wasm,
      mainWorker: mvp_worker,
    },
    eh: {
      mainModule: duckdb_wasm_eh,
      mainWorker: eh_worker,
    },
  };
  // Select a bundle based on browser checks
  const bundle = await duckdb.selectBundle(MANUAL_BUNDLES);
  // Instantiate the asynchronous version of DuckDB-wasm
  const worker = new Worker(bundle.mainWorker!);
  const logger = new duckdb.VoidLogger();

  db = new duckdb.AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
  return db;
};

const getConnection = async () => {
  db = await initDB();
  return db.connect();
};

const createTables = async (conn: AsyncDuckDBConnection) => {
  for (const table of Object.values(TABLES)) {
    const query = `CREATE TABLE ${table.tableName} AS SELECT * FROM '${table.source}'`;
    conn.query(query);
  }
};

const loadDB = async () => {
  const conn = await getConnection();
  createTables(conn);
}

export { getConnection, loadDB, TABLES };

