<script lang="ts">
	import { Table, TableBody, TableHead, TableHeadCell, Spinner } from 'flowbite-svelte';
	import AvgPriceTableRow from './AvgPriceTableRow.svelte';
	import { getConnection, PARQUETS } from '$lib/duckdb';

	import { selectedItemId } from '$lib/store';

	const getRows = async (itemId: string): Promise<AvgPriceRowData[]> => {
		const conn = await getConnection();
		const stmt = await conn.prepare(`
            SELECT 
                category, 
                ("2018" / 100)::FLOAT AS wtAvg2018, 
                ("2019" / 100)::FLOAT AS wtAvg2019, 
                ("2020" / 100)::FLOAT AS wtAvg2020, 
                ("2021" / 100)::FLOAT AS wtAvg2021, 
                ("2022" / 100)::FLOAT AS wtAvg2022, 
                ("2023" / 100)::FLOAT AS wtAvg2023
            FROM parquet_scan(${PARQUETS.itemWeightedAvgByYear})
            WHERE item_id = ?
            ORDER BY category DESC`);
		const results = await stmt.query(itemId);
		return results.toArray();
	};

	$: rows = getRows($selectedItemId);
	const headers = ['Type', '2023', '2022', '2021', '2020', '2019', '2018'];
</script>

{#await rows}
	<div class="flex items-center justify-center mt-5">
		<Spinner size="12" />
	</div>
{:then rows}
	<p class="dark:text-white text-xl text-center">Weighted Average Unit Price By Year</p>
	<Table hoverable class="mt-5">
		<TableHead theadClass="text-sm uppercase">
			{#each headers as header}
				<TableHeadCell>{header}</TableHeadCell>
			{/each}
		</TableHead>
		<TableBody tableBodyClass="divide-y">
			{#each rows as rowData}
				<AvgPriceTableRow {rowData} />
			{/each}
		</TableBody>
	</Table>
{/await}
