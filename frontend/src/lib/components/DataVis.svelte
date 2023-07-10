<script>
	import { Tabs, TabItem } from 'flowbite-svelte';
	import AvgPriceTable from './AvgPriceTable.svelte';
	import UnitPriceHistogram from './plots/UnitPriceHistogram.svelte';
	const handleClick = () => {
		// scroll to results
		const el = document.getElementById('view-bids');
		if (!el) return;
		el.scrollIntoView({ behavior: 'smooth', block: 'start' });
	};
</script>

<Tabs style="underline">
	<TabItem on:click={handleClick} open title="Weighted Average">
		<AvgPriceTable />
	</TabItem>
	<TabItem on:click={handleClick} title="Unit Price Histogram">
		<UnitPriceHistogram />
	</TabItem>
</Tabs>
