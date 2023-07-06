<script lang="ts">
	import { Table, TableBody, TableHead, TableHeadCell, Spinner } from 'flowbite-svelte';
	import ItemTableRow from './ItemTableRow.svelte';
	import { getConnection, getQueryResults, PARQUETS } from '$lib/duckdb';

	export let submittedSearchValue: string;
	export let submittedSpecYear: number;
	let limit = 10;
	let offset = 0;

	const prepareQuery = (
		submittedSearchValue: string,
		submittedSpecYear: number,
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
            in_spec_${submittedSpecYear} = TRUE AND
            (
                item_number LIKE '%${submittedSearchValue}%' OR
                long_description LIKE '%${submittedSearchValue}%'
            )
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

	$: rows = getRows(submittedSearchValue, submittedSpecYear, limit, offset);
	const headers = ['View Bids', 'Item Number', 'Item Description', 'Unit', 'Contract Occurrences'];
</script>

{#await rows}
	<div class="flex items-center justify-center mt-5">
		<Spinner size="12" />
	</div>
{:then rows}
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
{/await}
