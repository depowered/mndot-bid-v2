<script lang="ts">
	import { TableBodyCell, TableBodyRow } from 'flowbite-svelte';

	export let rowData: AvgPriceRowData;

	const formatFloat = (f: number) => {
		return f == null ? '--' : `$${f.toFixed(2)}`;
	};

	const tdClass = 'px-6 py-2 whitespace-nowrap font-medium ';
</script>

<TableBodyRow>
	{#if rowData.category == 'engineers'}
		<TableBodyCell {tdClass}>Engineer's Estimate</TableBodyCell>
	{:else if rowData.category == 'winning'}
		<TableBodyCell {tdClass}>Winning Bids</TableBodyCell>
	{:else}
		<TableBodyCell {tdClass}>Losing Bids</TableBodyCell>
	{/if}
	<TableBodyCell {tdClass}>{formatFloat(rowData.wtAvg2023)}</TableBodyCell>
	<TableBodyCell {tdClass}>{formatFloat(rowData.wtAvg2022)}</TableBodyCell>
	<TableBodyCell {tdClass}>{formatFloat(rowData.wtAvg2021)}</TableBodyCell>
	<TableBodyCell {tdClass}>{formatFloat(rowData.wtAvg2020)}</TableBodyCell>
	<TableBodyCell {tdClass}>{formatFloat(rowData.wtAvg2019)}</TableBodyCell>
	<TableBodyCell {tdClass}>{formatFloat(rowData.wtAvg2018)}</TableBodyCell>
</TableBodyRow>
