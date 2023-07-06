import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import mvp_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
import duckdb_wasm_eh from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';

import type { AsyncDuckDB } from '@duckdb/duckdb-wasm'

let db: AsyncDuckDB | null = null;

const PARQUETS = {
  items: 'prod_item_search.parquet',
  bids: 'prod_bids.parquet',
  itemWeightedAvgByYear: 'prod_item_weighted_avg_by_year.parquet'
}

// Setup and connect to the database
const registerParquets = async (db: AsyncDuckDB) => {
  for (const parquet of Object.values(PARQUETS)) {
    await db.registerFileURL(parquet, `/${parquet}`, 4, false);
  }
};

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
  const logger = new duckdb.ConsoleLogger();

  db = new duckdb.AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
  await registerParquets(db)
  return db;
};

const getConnection = async () => {
  db = await initDB();
  return db.connect();
};

export { getConnection, PARQUETS };

