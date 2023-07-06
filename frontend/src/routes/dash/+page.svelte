<script lang="ts">
	import ItemTable from '../../lib/components/ItemTable.svelte';
	import ItemSearch from '../../lib/components/ItemSearch.svelte';

	import { selectedItemId } from '$lib/store';

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
</div>
{#if $selectedItemId}
	<h1 class="dark:text-white">Item Id: {$selectedItemId}</h1>
{/if}

<style>
	#dashboard {
		display: flex;
		flex-direction: column;
	}
</style>
