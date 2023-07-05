<script lang="ts">
	import { Button, TableBodyCell, TableBodyRow } from 'flowbite-svelte';
	import ViewBidsBtn from './ViewBidsBtn.svelte';

	export let id: number;
	export let itemNumber: string;
	export let itemDescription: string;
	export let unit: string;
	export let contractOccur: number;

	const tdClass = 'px-6 py-2 whitespace-nowrap font-medium ';
</script>

<TableBodyRow>
	<TableBodyCell {tdClass}>
		{#if contractOccur < 1}
			<ViewBidsBtn disabled={true} />
		{:else}
			<ViewBidsBtn />
		{/if}
	</TableBodyCell>
	<TableBodyCell {tdClass}>{itemNumber}</TableBodyCell>
	<TableBodyCell {tdClass}>{itemDescription}</TableBodyCell>
	<TableBodyCell {tdClass}>{unit}</TableBodyCell>
	<TableBodyCell {tdClass}>{contractOccur}</TableBodyCell>
</TableBodyRow>
