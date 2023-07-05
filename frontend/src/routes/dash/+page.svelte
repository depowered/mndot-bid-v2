<script>
	import ItemTable from '../../lib/components/ItemTable.svelte';
	import ItemSearch from '../../lib/components/ItemSearch.svelte';
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
