<script lang="ts">
	import { Table, TableBody, TableHead, TableHeadCell, Spinner, P } from 'flowbite-svelte';
	import AvgPriceTableRow from './AvgPriceTableRow.svelte';

	import { weightedAvgPrices } from '$lib/store';
</script>

{#await $weightedAvgPrices}
	<div class="flex items-center justify-center mt-5">
		<Spinner size="12" />
	</div>
{:then $weightedAvgPrices}
	<p class="dark:text-white text-xl text-center">Weighted Average Unit Price By Year</p>
	<P class="mt-2" weight="light" color="text-black dark:text-gray-300">
		The averages shown below are calculated in a similar way to those in the published
		<a
			class="underline hover:no-underline"
			href="https://edocs-public.dot.state.mn.us/edocs_public/DMResultSet/Urlsearch?columns=docnumber,docname,app_id&folderid=28521650"
			target="_blank">Average Bid Price</a
		> documents. These values may differ slightly from the published values as some abstracts (less than
		1%) are excluded from this dataset.
	</P>
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
