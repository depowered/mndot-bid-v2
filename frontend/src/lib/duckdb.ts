import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import mvp_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
import duckdb_wasm_eh from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';

import type { AsyncDuckDB } from '@duckdb/duckdb-wasm'

const BUCKET = 'https://r2.mndotbidprices.com'

enum Parquet {
  ITEMS = 'prod_item_search.parquet',
  BIDS = 'prod_bids.parquet',
  WT_AVG_BY_YEAR = 'prod_item_weighted_avg_by_year.parquet',
}

type RemoteParquet = {
  name: string;
  url: string;
};

const REMOTE_PARQUETS: RemoteParquet[] = [
  { name: Parquet.ITEMS, url: `${BUCKET}/${Parquet.ITEMS}` },
  { name: Parquet.BIDS, url: `${BUCKET}/${Parquet.BIDS}` },
  { name: Parquet.WT_AVG_BY_YEAR, url: `${BUCKET}/${Parquet.WT_AVG_BY_YEAR}` }
]

type FileBuffer = {
  name: string;
  buffer: Uint8Array;
}

const fetchParquets = async (parquets: RemoteParquet[]): Promise<FileBuffer[]> => {
  return Promise.all(parquets.map(async (p) => {
    const res = await fetch(p.url);
    return {
      name: p.name,
      buffer: new Uint8Array(await res.arrayBuffer())
    };
  }))
}

const registerParquets = async (db: AsyncDuckDB, fileBuffers: FileBuffer[]) => {
  fileBuffers.forEach((f) => { db.registerFileBuffer(f.name, f.buffer) });
}

// Declare globally so that initDB can short circuit if the database has been initialized
let db: AsyncDuckDB | null = null;

const initDB = async () => {
  if (db) {
    return db;  // Return existing db if already initialized
  }

  // Load bundles from CDN (jsdelivr)
  const JSDELIVR_BUNDLES = duckdb.getJsDelivrBundles();

  // Select a bundle based on browser checks
  const bundle = await duckdb.selectBundle(JSDELIVR_BUNDLES);

  const worker_url = URL.createObjectURL(
    new Blob([`importScripts("${bundle.mainWorker!}");`], { type: 'text/javascript' })
  );

  // Instantiate the asynchronus version of DuckDB-Wasm
  const worker = new Worker(worker_url);
  const logger = new duckdb.ConsoleLogger();
  db = new duckdb.AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
  URL.revokeObjectURL(worker_url);

  // Fetch and register remote parquet files
  const fileBuffers = await fetchParquets(REMOTE_PARQUETS);
  await registerParquets(db, fileBuffers);

  return db;
};

const getConnection = async () => {
  db = await initDB();
  return db.connect();
};


export { initDB, getConnection, Parquet };

