<script lang="ts">
	import { Button, TableBodyCell, TableBodyRow } from 'flowbite-svelte';
	import { selectedItemId } from '$lib/store';

	export let rowData: ItemRowData;

	const handleClick = () => {
		selectedItemId.set(rowData.id);
	};

	const tdClass = 'px-6 py-2 whitespace-nowrap font-medium ';
</script>

<TableBodyRow>
	<TableBodyCell {tdClass}>
		{#if rowData.contractOccur < 1}
			<Button disabled={true} class="w-8 h-8 p-0">
				<img src="/xmark-solid.svg" alt="x icon" class="h-5 w-5" />
			</Button>
		{:else}
			<Button on:click={handleClick} class="w-8 h-8 p-0">
				<img src="/chart-icon.svg" alt="chart icon" class="h-5 w-5" />
			</Button>
		{/if}
	</TableBodyCell>
	<TableBodyCell {tdClass}>{rowData.itemNumber}</TableBodyCell>
	<TableBodyCell {tdClass}>{rowData.itemDescription}</TableBodyCell>
	<TableBodyCell {tdClass}>{rowData.unit}</TableBodyCell>
	<TableBodyCell {tdClass}>{rowData.contractOccur}</TableBodyCell>
</TableBodyRow>
