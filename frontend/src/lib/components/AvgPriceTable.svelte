<script lang="ts">
	import { Table, TableBody, TableHead, TableHeadCell, Spinner } from 'flowbite-svelte';
	import AvgPriceTableRow from './AvgPriceTableRow.svelte';

	import { weightedAvgPrices } from '$lib/store';
</script>

{#await $weightedAvgPrices}
	<div class="flex items-center justify-center mt-5">
		<Spinner size="12" />
	</div>
{:then $weightedAvgPrices}
	<p class="dark:text-white text-xl text-center">Weighted Average Unit Price By Year</p>
	<Table hoverable class="mt-5">
		<TableHead theadClass="text-sm uppercase">
			{#each $weightedAvgPrices.headers as header}
				<TableHeadCell>{header}</TableHeadCell>
			{/each}
		</TableHead>
		<TableBody tableBodyClass="divide-y">
			{#each $weightedAvgPrices.data as rowData}
				<AvgPriceTableRow {rowData} />
			{/each}
		</TableBody>
	</Table>
{/await}
