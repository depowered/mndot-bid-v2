<script lang="ts">
	import { Table, TableBody, TableHead, TableHeadCell } from 'flowbite-svelte';
	import ItemTableRow from './ItemTableRow.svelte';

	const headers = ['Item Number', 'Item Description', 'Unit', 'Contract Occurances'];

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
		<TableHeadCell />
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
