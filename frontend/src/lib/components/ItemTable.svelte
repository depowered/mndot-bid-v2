<script lang="ts">
	import { Table, TableBody, TableHead, TableHeadCell } from 'flowbite-svelte';
	import ItemTableRow from './ItemTableRow.svelte';
	import { initDB } from '../duckdb';
	import type { AsyncDuckDBConnection } from '@duckdb/duckdb-wasm';

	const headers = ['View Data', 'Item Number', 'Item Description', 'Unit', 'Contract Occurances'];

	// Setup and connect to the database
	let conn_prom: Promise<AsyncDuckDBConnection> | null; // Declare globally so promise can be awaited anywhere
	const load_db = async () => {
		if (conn_prom) {
			return conn_prom; // Return existing promise, if any
		}

		// Initialize database
		const db = await initDB();
		await db.registerFileURL('part-0.parquet', parquetUrl, 4, false); // From: https://voltrondata-labs-datasets.s3.us-east-2.amazonaws.com/nyc-taxi-tiny/year=2009/month=1/part-0.parquet

		conn_prom = db.connect(); // Open a connection (promise)
		return conn_prom;
	};

	// SQL to send to DuckDB-Wasm
	const viz_query = `
      SELECT date_trunc('day', pickup_datetime) as pickup_date, AVG(total_amount) as total_amount
      FROM parquet_scan('part-0.parquet') -- Use same filename as passed in registerFileUrl
      GROUP BY pickup_date
    `;

	// Send query and await results from DuckDB
	const get_query = async (q: string) => {
		const conn = await conn_prom;
		const results = await conn.query(q);
		return results;
	};

	let rows = [
		{
			id: 1,
			itemNumber: '2100.501/00010',
			itemDescription: 'MOBILIZATION',
			unit: 'L SUM',
			contractOccur: 10
		},
		{
			id: 2,
			itemNumber: '2106.501/00901',
			itemDescription: 'COMMON EXCAVATION',
			unit: 'CU YD',
			contractOccur: 50
		},
		{
			id: 3,
			itemNumber: '2575.503/00041',
			itemDescription: 'SEDIMENT CONTROL LOG TYPE COMPOST',
			unit: 'LIN FT',
			contractOccur: 25
		},
		{
			id: 4,
			itemNumber: '2575.601/00015',
			itemDescription: 'LIVE STAKES',
			unit: 'EACH',
			contractOccur: 0
		}
	];
</script>

<Table hoverable class="mt-5">
	<TableHead theadClass="text-sm uppercase">
		{#each headers as header}
			<TableHeadCell>{header}</TableHeadCell>
		{/each}
	</TableHead>
	<TableBody tableBodyClass="divide-y">
		{#each rows as row}
			<ItemTableRow {...row} />
		{/each}
	</TableBody>
</Table>
