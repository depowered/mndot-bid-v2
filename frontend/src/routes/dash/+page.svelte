<script>
	import ItemTable from './ItemTable.svelte';
	import ItemSearch from './itemSearch.svelte';
</script>

<div id="dashboard">
	<ItemSearch />
	<ItemTable />
</div>

<style>
	#dashboard {
		display: flex;
		flex-direction: column;
	}
</style>
