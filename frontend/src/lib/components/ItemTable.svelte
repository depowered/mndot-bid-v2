<script lang="ts">
	import { Table, TableBody, TableHead, TableHeadCell, Spinner, Pagination } from 'flowbite-svelte';
	import ItemTableRow from './ItemTableRow.svelte';
	import { getConnection, getQueryResults, PARQUETS } from '$lib/duckdb';

	export let submittedSearchValue: string;
	export let submittedSpecYear: number;
	let limit = 10;
	let offset = 0;

	const prepareSubQuery = (submittedSearchValue: string, submittedSpecYear: number) => {
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
        ORDER BY item_number`;
	};

	const getRecordCount = async (subQuery: string): Promise<number> => {
		const conn = await getConnection();
		const q = `SELECT COUNT(*) AS count FROM (${subQuery})`;
		const results = await getQueryResults(conn, q);
		return results.toArray()[0].count;
	};

	const getRows = async (subQuery: string, limit: number, offset: number) => {
		const conn = await getConnection();
		const q = `SELECT * FROM (${subQuery}) LIMIT ${limit} OFFSET ${offset}`;
		const results = await getQueryResults(conn, q);
		return results.toArray();
	};

	$: subQuery = prepareSubQuery(submittedSearchValue, submittedSpecYear);

	// Table content
	$: rows = getRows(subQuery, limit, offset);
	const headers = ['View Bids', 'Item Number', 'Item Description', 'Unit', 'Contract Occurrences'];

	// Pagination
	// Reset the value of offset on new search to reset paging
	const resetOffset = (submittedSearchValue: string) => 0;
	$: offset = resetOffset(submittedSearchValue);

	$: recordCount = getRecordCount(subQuery);
	const previous = () => {
		offset - limit >= limit ? (offset -= limit) : (offset = 0);
	};
	const next = async () => {
		const max = await recordCount;
		offset + limit < max ? (offset += limit) : (offset = offset);
	};
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
{#await recordCount then recordCount}
	<div class="flex flex-col items-center justify-center gap-2">
		<div class="text-sm text-gray-700 dark:text-gray-400">
			Showing <span class="font-semibold text-gray-900 dark:text-white">{offset + 1}</span> to
			<span class="font-semibold text-gray-900 dark:text-white"
				>{offset + limit < recordCount ? offset + limit : recordCount}</span
			>
			of <span class="font-semibold text-gray-900 dark:text-white">{recordCount}</span> Entries
		</div>

		<Pagination table on:previous={previous} on:next={next}>
			<span slot="prev">Prev</span>
		</Pagination>
	</div>
{/await}
