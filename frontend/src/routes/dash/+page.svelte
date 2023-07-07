<script lang="ts">
	import ItemTable from '../../lib/components/ItemTable.svelte';
	import ItemSearch from '../../lib/components/ItemSearch.svelte';

	import { selectedItemId } from '$lib/store';
	import DataVis from '$lib/components/DataVis.svelte';

	let defaultSearchValue = '';
	let defaultSpecYear = 2020;
	let submittedSearchValue: string;
	let submittedSpecYear: number;
</script>

<div id="dashboard">
	<ItemSearch
		searchValue={defaultSearchValue}
		specYear={defaultSpecYear}
		bind:submittedSearchValue
		bind:submittedSpecYear
	/>
	<ItemTable bind:submittedSearchValue bind:submittedSpecYear />
	{#if $selectedItemId}
		<DataVis />
	{/if}
</div>

<style>
	#dashboard {
		display: flex;
		flex-direction: column;
	}
</style>
