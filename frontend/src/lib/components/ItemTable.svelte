<script lang="ts">
	import { Table, TableBody, TableHead, TableHeadCell } from 'flowbite-svelte';
	import ItemTableRow from './ItemTableRow.svelte';
	import { getConnection, getQueryResults, PARQUETS } from '$lib/duckdb';

	const prepareQuery = (
		searchValue: string,
		selectedSpecYear: number,
		limit: number,
		offset: number
	) => {
		return `
        SELECT 
            id, 
            item_number as itemNumber, 
            long_description as itemDescription,
            plan_unit_description as unit,
            contract_count as contractOccur
        FROM parquet_scan(${PARQUETS.items})
        WHERE 
            in_spec_${selectedSpecYear} = TRUE AND
            item_number LIKE '%${searchValue}%' OR
            long_description LIKE '%${searchValue}%'
        ORDER BY item_number
        LIMIT ${limit}
        OFFSET ${offset}
        `;
	};

	const getRows = async (
		searchValue: string,
		selectedSpecYear: number,
		limit: number,
		offset: number
	) => {
		const conn = await getConnection();
		const q = prepareQuery(searchValue, selectedSpecYear, limit, offset);
		const results = await getQueryResults(conn, q);
		return results.toArray();
	};

	export let searchValue = '';
	export let selectedSpecYear = 2020;
	export let limit = 10;
	export let offset = 0;

	$: rows = getRows(searchValue, selectedSpecYear, limit, offset);
	const headers = ['View Bids', 'Item Number', 'Item Description', 'Unit', 'Contract Occurrences'];
</script>

<Table hoverable class="mt-5">
	<TableHead theadClass="text-sm uppercase">
		{#each headers as header}
			<TableHeadCell>{header}</TableHeadCell>
		{/each}
	</TableHead>
	{#await rows}
		<div />
	{:then rows}
		<TableBody tableBodyClass="divide-y">
			{#each rows as row}
				<ItemTableRow {...row} />
			{/each}
		</TableBody>
	{/await}
</Table>
