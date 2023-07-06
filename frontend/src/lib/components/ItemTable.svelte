<script lang="ts">
	import { Table, TableBody, TableHead, TableHeadCell } from 'flowbite-svelte';
	import ItemTableRow from './ItemTableRow.svelte';
	import { initDB } from '$lib/duckdb';

	// Setup and connect to the database
	const load_db = async () => {
		console.log('LOADING DB');
		// Initialize database
		const db = await initDB();
		await db.registerFileURL('prod_item_search.parquet', '/prod_item_search.parquet', 4, false);
		const conn = db.connect(); // Open a connection (promise)
		return conn;
	};

	// Set up the db connection as an empty promise.
	const conn_prom = load_db();

	// SQL to send to DuckDB-Wasm
	const prepare_query = (searchValue = '', selectedSpecYear = 2020, limit = 20, offset = 0) => {
		return `
        SELECT 
            id, 
            item_number as itemNumber, 
            long_description as itemDescription,
            plan_unit_description as unit,
            contract_count as contractOccur
        FROM parquet_scan('prod_item_search.parquet')
        WHERE 
            in_spec_${selectedSpecYear} = TRUE AND
            item_number LIKE '%${searchValue}%' OR
            long_description LIKE '%${searchValue}%'
        ORDER BY item_number
        LIMIT ${limit}
        OFFSET ${offset}
        `;
	};

	// Send query and await results from DuckDB
	const get_query = async (q: string) => {
		const conn = await conn_prom;
		const results = await conn.query(q);
		return results;
	};

	const headers = ['View Bids', 'Item Number', 'Item Description', 'Unit', 'Contract Occurrences'];
	let rows = new Promise(() => {});

	const get_rows = async (searchValue = '', selectedSpecYear = 2020, limit = 20, offset = 0) => {
		const q = prepare_query(searchValue, selectedSpecYear, limit, offset);
		console.log(q);
		const results = get_query(q);
		const result = await results;
		rows = result.toArray();
	};

	conn_prom.then(() => get_rows());
</script>

<Table hoverable class="mt-5">
	<TableHead theadClass="text-sm uppercase">
		{#each headers as header}
			<TableHeadCell>{header}</TableHeadCell>
		{/each}
	</TableHead>
	{#await rows}
		<div />
	{:then}
		<TableBody tableBodyClass="divide-y">
			{#each rows as row}
				<ItemTableRow {...row} />
			{/each}
		</TableBody>
	{/await}
</Table>
